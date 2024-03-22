"""
Microservice for a privacy preserving LLM assistant.

The following program reads in a collection of documents from local directory,
embeds each document using a locally deployed SentenceTransformer,
then builds an index for fast retrieval of documents relevant to a question,
effectively replacing a vector database.

The program then starts a REST API endpoint serving queries about programming in Pathway.

Each query text is first turned into a vector using the SentenceTransformer,
then relevant documentation pages are found using a Nearest Neighbor index computed
for documents in the corpus. A prompt is build from the relevant documentations pages
and run through a local LLM downloaded form the HuggingFace repository.

Usage:
In the root of this repository run:
`poetry run ./run_examples.py local`
or, if all dependencies are managed manually rather than using poetry
`python examples/pipelines/local/app.py`

You can also run this example directly in the environment with llm_app instaslled.

To call the REST API:
curl --data '{"user": "user", "query": "Where do I live?"}' http://localhost:8080/ | jq
"""
import os

import pathway as pw
from pathway.stdlib.ml.index import KNNIndex

from llm_app.model_wrappers import SentenceTransformerTask, LiteLLMChatModel

from dotenv import load_dotenv
load_dotenv()


class DocumentInputSchema(pw.Schema):
    doc: str


class QueryInputSchema(pw.Schema):
    query: str
    user: str


def run(
    *,
    data_dir: str = os.environ.get(
        "PATHWAY_DATA_DIR", "llm/data/pathway-docs-small"
    ),
    host: str = os.getenv("PATHWAY_BASEURL"),
    port: int = int(os.getenv("PATHWAY_PORT")),
    embedder_locator: str = os.environ.get("EMBEDDER", "intfloat/e5-large-v2"),
    embedding_dimension: int = 1024,
    max_tokens: int = 0,
    device: str = "cpu",
    **kwargs,
):
    embedder = SentenceTransformerTask(model=embedder_locator, device=device)
    embedding_dimension = len(embedder(""))

    documents = pw.io.jsonlines.read(
        data_dir,
        schema=DocumentInputSchema,
        mode="streaming",
        autocommit_duration_ms=50,
    )

    enriched_documents = documents + documents.select(
        vector=embedder.apply(text=pw.this.doc)
    )

    index = KNNIndex(
        enriched_documents.vector, enriched_documents, n_dimensions=embedding_dimension
    )

    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
        delete_completed_queries=True,
    )

    query += query.select(
        vector=embedder.apply(text=pw.this.query),
    )

    query_context = query + index.get_nearest_items(
        query.vector, k=3, collapse_rows=True
    ).select(documents_list=pw.this.doc)

    @pw.udf
    def build_prompt(documents, query):
        docs_str = "\n".join(documents)
        prompt = f"Given the following documents : \n {docs_str} \nOutline the route travelled and mention the temperatures throughout the day, travel advisories and precautions to take while travelling this route :{query} "
        return prompt

    prompt = query_context.select(
        prompt=build_prompt(pw.this.documents_list, pw.this.query)
    )
    os.environ["OPENAI_API_KEY"] = "RandomText"
    model = LiteLLMChatModel()

    responses = prompt.select(
        query_id=pw.this.id,
        result=model.apply(
            pw.this.prompt, max_tokens=max_tokens, custom_llm_provider="custom_openai",base_url="http://0.0.0.0:8000/v1",locator="custom_openai"
        ),
    )

    response_writer(responses)

    pw.run()


if __name__ == "__main__":
    run()
