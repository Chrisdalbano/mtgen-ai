<template>
  <div class="flex justify-center content-center" @mousemove="handleMouseMove">
    <div
      class="card-container"
      ref="cardContainer"
      :style="{
        backgroundImage: 'url(' + cardFrame + ')',
        transform: `rotateX(${position.y}deg) rotateY(${position.x}deg)`
      }"
    >
      <div class="card-name font-belerenbold text-black">
        {{ cardTitle }}
      </div>
      <div
        class="card-cost mana-symbol flex flex-row text-black"
        v-html="formatCost(cardCost)"
      ></div>
      <div
        class="card-art"
        :style="{ backgroundImage: 'url(' + cardArt + ')' }"
      >
        <div class="generated-art" :style="{ width: '152px' }"></div>
      </div>
      <div class="card-type font-jacebeleren text-black font-semibold">
        {{ cardType }}
      </div>
      <div
        class="card-description font-mplantin text-black p-0.5"
        ref="cardDescription"
        :style="{ fontSize: fontSize + 'px' }"
        v-html="formattedDescription"
      ></div>
      <div class="card-power text-black font-jacebeleren">
        {{ cardPower }}/{{ cardToughness }}
      </div>
    </div>
  </div>
</template>

<script>
import redFrame from "@/assets/card-frames/red-frame.png";
import blueFrame from "@/assets/card-frames/blue-frame.png";
import blackFrame from "@/assets/card-frames/black-frame.png";
import greenFrame from "@/assets/card-frames/green-frame.png";
import whiteFrame from "@/assets/card-frames/white-frame.png";
import multicoloredFrame from "@/assets/card-frames/multicolored-frame.png";

export default {
  name: "CardComponent",
  props: {
    cardTitle: {
      type: String,
      default: "",
    },
    cardType: {
      type: String,
      default: "",
    },
    cardArt: {
      type: String,
      default: "",
    },
    cardCost: {
      type: String,
      default: "",
    },
    cardDescription: {
      type: String,
      default: "",
    },
    cardPower: {
      type: String,
      default: "",
    },
    cardToughness: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      fontSize: 11, // Initial font size
      redFrame,
      blueFrame,
      blackFrame,
      greenFrame,
      whiteFrame,
      multicoloredFrame,
      position: { x: 0, y: 0 }, // Initial position for the parallax effect
    };
  },
  methods: {
    handleMouseMove(e) {
      this.position.x = (e.pageX - this.$refs.cardContainer.offsetLeft - (this.$refs.cardContainer.offsetWidth / 2)) / 10;
      this.position.y = -1 * (e.pageY - this.$refs.cardContainer.offsetTop - (this.$refs.cardContainer.offsetHeight / 2)) / 10;
    },
    formatCost(cost) {
      const symbols = cost.match(/{[^{}]+}/g) || [];
      symbols.forEach((symbol) => {
        const iconSrc = this.getSymbol(symbol);
        const iconTag = `<img src="${iconSrc}" class="mana-symbol" />`;
        cost = cost.replace(symbol, iconTag);
      });
      return cost;
    },
    formatDescription(description) {
      const symbols = description.match(/{[^{}]+}/g) || [];
      symbols.forEach((symbol) => {
        const iconSrc = this.getSymbol(symbol);
        const iconTag = `<img src="${iconSrc}" class="description-symbol" style="display: inline-block; vertical-align: middle; width: 11px; height: 11px;" />`;
        description = description.replace(symbol, iconTag);
      });
      // Replace '\n' with <br/>
      description = description.replace(/\\n/g, "<br/>");
      // Wrap the formatted description in a paragraph tag
      description = `<p>${description}</p>`;
      return description;
    },
    isSymbol(el) {
      return el.startsWith("{") && el.endsWith("}");
    },
    getSymbol(symbol) {
      const iconName = symbol.replace(/[{}]/g, "");
      return require(`@/assets/mtg-icons/${iconName}.png`);
    },

    adjustFontSize() {
      const cardDescriptionElement = this.$refs.cardDescription;
      const maxIterations = 10; // Maximum number of iterations to reduce font size
      let iterations = 0;

      while (
        cardDescriptionElement.scrollHeight >
          cardDescriptionElement.clientHeight &&
        iterations < maxIterations
      ) {
        this.fontSize -= 1;
        iterations++;
      }
    },
  },

  computed: {
    formattedDescription() {
      return this.formatDescription(this.cardDescription);
    },
    titleCharCount() {
      return this.cardTitle.length;
    },
    charCount() {
      return this.cardDescription.length;
    },
    parsedCost() {
      return this.cardCost.split(/(?<=})|(?={)/g);
    },
    cardFrame() {
      if (this.cardCost.includes("R")) return this.redFrame;
      if (this.cardCost.includes("U")) return this.blueFrame;
      if (this.cardCost.includes("B")) return this.blackFrame;
      if (this.cardCost.includes("G")) return this.greenFrame;
      if (this.cardCost.includes("W")) return this.whiteFrame;
      return this.multicoloredFrame;
    },
  },
  watch: {
    titleCharCount(newCount) {
      if (newCount > 18) {
        this.fontSize = 9;
      } else {
        this.fontSize = 11;
      }
    },
    charCount(newCount) {
      if (newCount > 181) {
        this.fontSize = 9;
      } else {
        this.fontSize = 11;
      }
    },
    cardDescription: {
      handler() {
        this.$nextTick(this.adjustFontSize);
      },
      immediate: true,
    },
  },
  created() {
    // Check the initial character count
    if (this.charCount > 181) {
      this.fontSize = 9;
    }
    if (this.titleCharCount > 18) {
      this.fontSize = 9;
    }
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Bad+Script&display=swap");

.card-container {
  background-size: contain;
  width: 250px;
  height: 349px;
  position: relative;
  color: white;
  padding: 10px;
  box-sizing: border-box;
}

.card-name {
  /* border: solid red 1px; */
  position: absolute;
  top: 20px;
  left: 25px;
  font-size: 12px; /* you can adjust this as needed */
  cursor: default;
}

.card-cost {
  position: absolute;
  top: 20px;
  right: 38px;
  margin-right: 10px;
}

.card-type {
  /* border: solid red 1px; */
  position: absolute;
  top: 199px;
  left: 25px;
  font-size: 10px; /* you can adjust this as needed */
  cursor: default;
}

.card-description {
  /* border: solid red 1px; */
  position: absolute;
  top: 220px; /* this might be the middle of the card, adjust as needed */
  left: 22px;
  right: 24px; /* add some padding on the right side */
  bottom: 40px;
  font-size: 11px; /* adjust as needed */
  overflow: auto;
  cursor: default;
}

.card-power {
  position: absolute;
  bottom: 16px;
  right: 30px;
  font-size: 16px; 
  cursor: default;
}
.mana-symbol {
  width: 12px !important;
  height: 12px !important;
  margin-top: 1px;
  padding: 0;
  vertical-align: middle;
  
}

.description-symbol {
  width: 10px;
  height: 10px;
}

.card-art {
  position: absolute;
  top: 40px;
  left: 22px;
  right: 22px;
  bottom: 155px;
  font-size: 11px;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  width: 207px;
  height: 154px;
}
</style>
