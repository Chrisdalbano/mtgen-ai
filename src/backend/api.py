from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


class CardGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model_engine = "gpt-3.5-turbo"
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def generate_card(self, prompt):
        data = {
            "model": self.model_engine,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
        }

        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            gpt_output = response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

        return {
            "gpt_output": gpt_output,
        }


@app.route("/generate-card", methods=["POST"])
def generate_card():
    prompt = request.json["prompt"]
    card_generator = CardGenerator(
        "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"
    )
    card_info = card_generator.generate_card(prompt)
    return jsonify(card_info)


if __name__ == "__main__":
    app.run()
