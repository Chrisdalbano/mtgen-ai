const functions = require("firebase-functions");
const cors = require("cors")({ origin: true });
const fetch = require("node-fetch");
const admin = require("firebase-admin");
admin.initializeApp();

const api_key = functions.config().openai.api_key; // Ensure this is set in Firebase config
const headers = {
  "Content-Type": "application/json",
  Authorization: `Bearer ${api_key}`,
};

exports.generateCard = functions.https.onRequest((request, response) => {
  cors(request, response, async () => {
    if (request.method !== "POST") {
      return response.status(405).send("Method Not Allowed");
    }

    const { textPrompt, artPrompt } = request.body;
    try {
      const gptOutput = await generateText(textPrompt);
      const imageUrls = await generateImage(artPrompt);
      response.json({ gpt_output: gptOutput, image_urls: imageUrls });
    } catch (error) {
      console.error("Error in generating outputs:", error);
      response.status(500).send({
        message: "Internal server error",
        details: error.message,
        stack: error.stack,
      });
    }
  });
});

async function generateText(prompt) {
  const data = {
    model: "gpt-4-turbo",
    messages: [{ role: "user", content: prompt }],
    temperature: 0.8,
  };
  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });
    if (!response.ok)
      throw new Error(`API call failed with status ${response.status}`);
    return (await response.json()).choices[0].message.content;
  } catch (error) {
    console.error("Failed to generate text:", error);
    throw error; // Re-throw to handle it in the calling function
  }
}

async function generateImage(prompt) {
  // Updating the function to use dall-e-3 and potentially higher resolution
  const data = {
    model: "dall-e-3",  // Specify the model version
    prompt: prompt,      // Using the prompt passed to the function
    n: 1,                // Number of images to generate
    size: "1024x1024"    // Requesting a larger image size; adjust as needed
  };

  try {
    const response = await fetch(
      "https://api.openai.com/v1/images/generations",
      {
        method: "POST",
        headers: headers,  // Make sure the 'headers' variable includes your API key
        body: JSON.stringify(data),
      }
    );

    if (!response.ok) {
      throw new Error(`API call failed with status ${response.status}`);
    }

    const jsonResponse = await response.json();
    return jsonResponse.data.map((img) => img.url);
  } catch (error) {
    console.error("Failed to generate image:", error);
    throw error; // Re-throw the error for handling in the calling function
  }
}

