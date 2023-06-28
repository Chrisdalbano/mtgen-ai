from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()


class CardGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model_engine = "gpt-3.5-turbo"
        self.dalle_url = "https://api.openai.com/v1/images/generations"
        self.chat_url = "https://api.openai.com/v1/chat/completions"
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

        response = requests.post(
            self.chat_url, headers=self.headers, data=json.dumps(data)
        )

        if response.status_code == 200:
            gpt_output = response.json()["choices"][0]["message"]["content"]
            image_urls = self.generate_image(prompt)  # Generate the image URLs
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

        return {
            "gpt_output": gpt_output,
            "image_urls": image_urls,  # Include the image URLs in the response
        }

    def generate_image(self, prompt, n=1, size="1024x1024"):
        data = {
            "prompt": prompt,
            "n": n,
            "size": size,
        }

        response = requests.post(self.dalle_url, headers=self.headers, json=data)

        if response.status_code == 200:
            image_urls = [image["url"] for image in response.json()["data"]]
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

        return image_urls


@app.route("/generate-card", methods=["POST"])
def generate_card():
    prompt = request.json["prompt"]
    card_generator = CardGenerator(os.getenv("OPENAI_API_KEY"))
    card_info = card_generator.generate_card(prompt)
    return jsonify(card_info)


if __name__ == "__main__":
    app.run()
