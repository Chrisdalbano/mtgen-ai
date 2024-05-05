<template>
  <div
    class="flex flex-col items-center justify-center bg-gray-100"
    :style="'min-height: 90vh;'"
  >
    <h1 class="text-4xl lg:text-6xl font-belerenbold text-gray-200 mb-2">
      Magic The Generator
    </h1>
    <h2 class="text-base mb-4 text-gray-200">An AI MTG Card generator</h2>
    <div class="flex flex-col items-center">
      <input
        v-model="prompt"
        class="border border-gray-400 bg-gray-900 text-gray-200 font-jacebeleren rounded-sm px-4 py-2 w-80 mb-4"
        placeholder="Type your card"
        autocomplete="off"
      />
      <!-- <button @click="showApiKeyInput = !showApiKeyInput" class="text-gray-300 text-m font-mplantin px-4 py-2 m-2 rounded border-solid border-2 border-white">
        Add OpenAI API Key
      </button> -->
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
      <button
        @click="generateTestCard"
        class="bg-green-600 hover:bg-green-700 text-white rounded-sm font-belerenbold px-4 py-2 mt-2"
      >
        Generate Test Card
      </button>
      <div v-if="loading" class="spinner"></div>
    </div>
    <div class="mt-2">
      <CardComponent
        v-if="(cardTextLoaded && cardArtLoaded) || testCard"
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
      cardTextLoaded: false,
      cardArtLoaded: false,
      prompt: "",
      apiKey: "",
      showApiKeyInput: false,
      gptOutput: "",
      testCard: false,
      cardProperties: {
        name: "Test Dragon",
        cost: "5RR",
        type: "Creature - Dragon",
        power: "5",
        toughness: "5",
        abilities: "Flying, {T}: This creature deals 3 damage to any target.",
        art: "https://assetsio.gnwcdn.com/Mechanical_Whelp_full2.jpg?width=1920&height=1920&fit=bounds&quality=80&format=jpg&auto=webp",
      },
      regex:
        /^\*\*Name:\*\*\s*(.+?)\s*$(?:\r?\n)+^\*\*Mana Cost:\*\*\s*(.+?)\s*$(?:\r?\n)+^\*\*Type:\*\*\s*(.+?)\s*$(?:\r?\n)+^\*\*Power\/Toughness:\*\*\s*(.+?)\s*$(?:\r?\n)+^\*\*Abilities:\*\*\s*((?:.|\r?\n)+?)(?:$(?:\r?\n)?\*\*|$)/im,
    };
  },
  methods: {
    async generateCard() {
      this.loading = true;
      this.cardTextLoaded = false;
      this.cardArtLoaded = false;

      const textPrompt = `Generate a Magic: The Gathering card description. Prompt: ${this.prompt}. Format: **Name:** <name> **Mana Cost:** <cost> **Type:** <type> **Power/Toughness:** <power/toughness> **Abilities:** <Abilities with fitting smart mechanics related to the characters fictional lore>`;

      try {
        const textResponse = await this.fetchCardText(textPrompt);
        if (textResponse.ok) {
          const cardText = await textResponse.json();
          this.gptOutput = cardText.gpt_output;
          const matches = this.gptOutput.match(this.regex);
          if (matches) {
            this.cardProperties = {
              name: matches[1].trim(),
              cost: matches[2].trim(),
              type: matches[3].trim(),
              power: matches[4].split("/")[0].trim(),
              toughness: matches[4].split("/")[1].trim(),
              abilities: matches[5].trim(),
            };
            this.cardTextLoaded = true; // Set text loaded flag to true

            // Generate the art based on the type extracted
            const artPrompt = `Create an epic '${this.cardProperties.type}' being in a dynamic pose that is a fanmade of '${this.prompt}' , suitable for a High Fantasy Art style. Centered Character. 4:3 Aspect Ratio`;
            const artResponse = await this.fetchCardArt(artPrompt);
            if (artResponse.ok) {
              const artData = await artResponse.json();
              this.cardProperties.art = artData.image_urls[0];
              this.cardArtLoaded = true; // Set art loaded flag to true
            }
          }
        }
      } catch (error) {
        console.error("Failed to generate the card:", error);
        alert(
          "There was a problem generating the card. Check the console for more details."
        );
      } finally {
        this.loading = false;
        if (!this.cardTextLoaded || !this.cardArtLoaded) {
          alert("Failed to load all card components. Please try again.");
        }
      }
    },
    async fetchCardText(prompt) {
      return fetch(
        "https://us-central1-mtgen-host.cloudfunctions.net/generateCardText",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt }),
        }
      );
    },
    async fetchCardArt(prompt) {
      return fetch(
        "https://us-central1-mtgen-host.cloudfunctions.net/generateCardArt",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt }),
        }
      );
    },
    generateTestCard() {
      this.testCard = true;
      this.cardProperties = {
        name: "Test Dragon",
        cost: "5RR",
        type: "Creature - Dragon",
        power: "5",
        toughness: "5",
        abilities: "**Flying** {T}: This creature deals 3 damage to any target.",
        art: "https://assetsio.gnwcdn.com/Mechanical_Whelp_full2.jpg?width=1920&height=1920&fit=bounds&quality=80&format=jpg&auto=webp",
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
