<template>
  <div class="flex flex-col items-center justify-center h-screen bg-gray-100">
    <h1 class="text-4xl font-belerenbold text-gray-200 mb-2">
      Magic The Generator
    </h1>
    <h2 class="text-sm font-jacebeleren mb-4 text-gray-200">
      An AI MTG Card generator
    </h2>
    <div class="flex flex-col items-center">
      <input
        v-model="prompt"
        class="border border-gray-400 bg-gray-900 text-gray-200 font-jacebeleren rounded-sm px-4 py-2 w-80 mb-4"
        placeholder="Type your card"
        autocomplete="off"
      />
      <button
        @click="showApiKeyInput = !showApiKeyInput"
        class="text-gray-300 text-xs font-belerenbold px-4 py-2"
      >
        Add OpenAI API Key
      </button>
      <input
        v-if="showApiKeyInput"
        v-model="apiKey"
        type="password"
        class="border border-gray-400 bg-gray-900 text-gray-200 font-jacebeleren rounded-sm text-xs px-4 py-2 w-40 mb-4"
        placeholder="API key"
        autocomplete="off"
      />
      <button
        @click="generateCard"
        class="bg-orange-600 hover:bg-orange-700 text-gray-100 rounded-sm font-belerenbold px-4 py-2 mt-4"
        :disabled="loading"
      >
        Generate Card
      </button>
      <div v-if="loading" class="spinner"></div>
    </div>
    <div class="mt-2">
      <CardComponent
        v-if="gptOutput"
        :cardTitle="cardProperties.name"
        :cardCost="cardProperties.cost"
        :cardType="cardProperties.type"
        :cardDescription="cardProperties.abilities"
        :cardPower="cardProperties.power"
        :cardToughness="cardProperties.toughness"
        :cardArt="cardProperties.art"
      />
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
        art: "",
        toughness: "",
        abilities: "",
      },
      regex:
        /(.+?)\nMana Cost: (.+?)\nType: (.+?)\nPower\/Toughness: (.+?)\nAbilities: (.+)/s,
    };
  },
  methods: {
    createCardText(card) {
      let text = `
    ${card.cardName}
    ${card.cost}
    ${card.type}
    ${card.description}
    ${card.power}/${card.toughness}
  `;
      return text.trim();
    },
    async generateCard() {
      if (!this.prompt) {
        return;
      }

      this.loading = true;
      apiKey: "", (this.gptOutput = "");
      this.cardProperties = {
        name: "",
        cost: "",
        type: "",
        power: "",
        toughness: "",
        abilities: "",
        art: "", // Add the art property here
      };

      const prompt = `Generate a fan-made Magic: The Gathering creature card based on the theme '${this.prompt}'. The output should match the specified format given by the following regex pattern: ${this.regex}.

Adhere to the following guidelines:

Use the specific notation for all action symbols, enclosed in '{}'. For example, use '{T}' for the tap action and '{UT}' for the untap action.
Each paragraph or individual block of text should end with a newline character ('\n') to denote the start of a new line.
Exclude flavor text and explanation, DO NOT ADD ANY FLAVOR TEXT or any extra text.
Avoid generating images or graphics.
The card structure should reflect a traditional Magic: The Gathering card, ensuring clarity in the cost, type, and abilities of the card, exclude any flavor text or extra lore/descriptive text. Make sure that the text is clear and free of ambiguity for easy parsing and matching with the provided regex pattern.`;

      const artPrompt = `Magic The Gathering Creature Art of ${this.prompt}, with Magic The Gathering Art Style, creature should have action pose and thematic background.`;

      // const response = await fetch("http://127.0.0.1:5000/generate-card", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //     "X-API-Key": this.apiKey, // Include the API key in the request headers
      //   },
      //   body: JSON.stringify({ prompt, artPrompt }),
      // });

      const response = await fetch(
        "https://mtgenapi.azurewebsites.net/generate-card",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": this.apiKey, // Include the API key in the request headers
          },
          body: JSON.stringify({ prompt, artPrompt }),
        }
      );

      if (response.ok) {
        const cardInfo = await response.json();
        this.gptOutput = cardInfo.gpt_output;
        this.cardProperties.art = cardInfo.image_urls[0]; // Assign the first image URL to art property

        // Extract card properties using regular expressions
        const matches = this.gptOutput.match(this.regex);

        if (matches) {
          this.cardProperties = {
            name: matches[1].trim(),
            cost: matches[2].trim(),
            type: matches[3].trim(),
            power: matches[4].trim().split("/")[0],
            toughness: matches[4].trim().split("/")[1],
            abilities: matches[5].trim(),
            art: cardInfo.image_urls[0], // Assign the first image URL to art property
          };
        }
        this.loading = false;
      }
    },
    generateSampleCard() {
      this.gptOutput =
        "Sample Card\n\nMana Cost: 1 Red 1 Blue\n\nCard Type: Creature\n\nPower/Toughness: 2/2\n\nCard Text: This is a sample card generated by the app.\n\nFlavor Text: Enjoy!\n\nRarity: Common";
      this.cardProperties = {
        name: "Sample Card",
        cost: "1R1B",
        type: "Creature",
        power: "2",
        toughness: "2",
        abilities: "Sample abilities",
      };
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
  background: url("../assets/pics/mtgen-bg.png") no-repeat center center fixed;
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
