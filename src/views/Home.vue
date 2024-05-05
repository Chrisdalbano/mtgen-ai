<template>
  <div class="flex flex-col items-center justify-center bg-gray-100" :style="'min-height: 90vh;'">
    <h1 class="text-4xl lg:text-6xl font-belerenbold text-gray-200 mb-2">
      Magic The Generator
    </h1>
    <h2 class="text-base mb-4 text-gray-200">An AI MTG Card generator</h2>
    <div class="flex flex-col items-center">
      <input v-model="prompt" class="border border-gray-400 bg-gray-900 text-gray-200 font-jacebeleren rounded-sm px-4 py-2 w-80 mb-4" placeholder="Type your card" autocomplete="off" />
      <button @click="showApiKeyInput = !showApiKeyInput" class="text-gray-300 text-m font-mplantin px-4 py-2 m-2 rounded border-solid border-2 border-white">
        Add OpenAI API Key
      </button>
      <input v-if="showApiKeyInput" v-model="apiKey" type="password" class="border border-gray-400 bg-gray-900 text-gray-200 font-jacebeleren rounded-sm text-xs px-4 py-2 w-40 mb-4" placeholder="API key" autocomplete="off" />
      <button @click="generateCard" class="bg-orange-600 hover:bg-orange-700 text-gray-100 rounded-sm font-belerenbold px-4 py-2 mt-4" :disabled="loading">
        Generate Card
      </button>
      <div v-if="loading" class="spinner"></div>
    </div>
    <div class="mt-2">
      <CardComponent v-if="gptOutput" :cardTitle="cardProperties.name" :cardCost="cardProperties.cost" :cardType="cardProperties.type" :cardDescription="cardProperties.abilities" :cardPower="cardProperties.power" :cardToughness="cardProperties.toughness" :cardArt="cardProperties.art" />
    </div>
  </div>
</template>

<script>
import CardComponent from "@/components/CardComponent.vue";

export default {
  name: "Home",
  components: { CardComponent },
  data() {
    return {
      loading: false,
      prompt: "",
      apiKey: "",
      showApiKeyInput: false,
      gptOutput: "",
      cardProperties: {
        name: "",
        cost: "",
        type: "",
        power: "",
        toughness: "",
        abilities: "",
        art: "",
      },
      regex: /.*\*\*Name:\*\* (.+?)\n\*\*Mana Cost:\*\* (.+?)\n\*\*Type:\*\* (.+?)\n\*\*Power\/Toughness:\*\* (.+?)\n\*\*Abilities:\*\* ([\s\S]+?)(?:\n\*\*Flavor Text:.*|$)/,
    };
  },
  methods: {
    async generateCard() {
      if (!this.prompt) {
        alert("Please enter a prompt.");
        return;
      }

      this.loading = true;
      const textPrompt = `Generate a Magic: The Gathering card description for a creature. Use only the format provided below and exclude any additional text or elements. Creature name: '${this.prompt}'.
**Name:** <name>
**Mana Cost:** <cost>
**Type:** <type>
**Power/Toughness:** <power/toughness>
**Abilities:** <abilities>`;
      
      const artPrompt = `Create a fantastical creature in a dynamic pose based on fanmade ${this.prompt}, embodying themes of strength and mystery, suitable for a high fantasy card game. The creature should have distinctive features such as vibrant colors, mystical elements, and an imposing presence, and a fitting background to its theme.`;

      try {
        const response = await fetch(
          "https://us-central1-mtgen-host.cloudfunctions.net/generateCard",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ textPrompt, artPrompt }),
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const cardInfo = await response.json();
        this.gptOutput = cardInfo.gpt_output;
        const matches = this.gptOutput.match(this.regex);
        if (matches) {
          this.cardProperties = {
            name: matches[1].trim(),
            cost: matches[2].trim(),
            type: matches[3].trim(),
            power: matches[4].split("/")[0].trim(),
            toughness: matches[4].split("/")[1].trim(),
            abilities: matches[5].trim(),
            art: cardInfo.image_urls[0], // Assuming image URL is correctly fetched
          };
        } else {
          console.error("Regex did not match the output:", this.gptOutput);
          alert("Failed to parse card properties. Check the console for more details.");
        }
      } catch (error) {
        console.error("Failed to generate the card:", error);
        alert("There was a problem generating the card. Check the console for more details.");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
.card {
  width: 600px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-content {
  padding: 16px;
  text-align: center;
}

.text-med {
  font-size: 24px;
  line-height: 1.5;
}

.bg-gray-100 {
  background: url("../assets/pics/mtgen-bg.webp") no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
}

.spinner {
  margin-top: 1rem;
  border: 14px solid #220800;
  border-top: 14px solid #8f2a02;
  border-radius: 50%;
  width: 70px;
  height: 70px;
  animation: spin 0.4s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
