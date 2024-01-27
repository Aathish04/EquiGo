from llama_cpp.llama import Llama, LlamaGrammar
import json
grammar = LlamaGrammar.from_file("llm/grammar.gbnf")
llm = Llama("models/model.gguf")

def parseFreeText(text):
    response = llm(
        f"JSON of startlocation  endlocation  vehicletype  visionImpairment  mobilityPhysicalImpairment  hearingImpairment  breathingIssues  dyslexia given the following text: {text}",
        grammar=grammar, max_tokens=-1
    )
    response = json.loads(response['choices'][0]['text'])
    return response

print(parseFreeText("I would like to go from adyar to mylapore."))