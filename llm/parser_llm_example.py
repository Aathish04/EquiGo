import json
import requests

if __name__ == "__main__":
    text = "I would like to go from adyar to mylapore."
    prompt = f"JSON of startlocation  endlocation  vehicletype  visionImpairment  mobilityPhysicalImpairment  hearingImpairment  breathingIssues  dyslexia given the following text: {text}",
    with open("llm/grammar.gbnf") as f:
        grammar = f.read()

    res = requests.post(
        url="http://localhost:8000/v1/completions",
        json={
        "prompt" : prompt,
        "grammar" : grammar,
        "max_tokens":0
        }
    )
    print(json.loads(res.json()["choices"][0]["text"]))