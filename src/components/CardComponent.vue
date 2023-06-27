<template>
  <div class="flex justify-center content-center">
    <div
      class="card-container"
      ref="cardContainer"
      :style="{ backgroundImage: 'url(' + cardFrame + ')' }"
    >
      <div class="card-name font-serif text-black font-semibold">
        {{ cardTitle }}
      </div>
      <div class="card-cost text-black">
        {{ cardCost }}
      </div>
      <div class="card-type font-serif text-black font-semibold">
        {{ cardType }}
      </div>
      <div
        class="card-description font-serif text-black"
        ref="cardDescription"
        :style="{ fontSize: fontSize + 'px' }"
      >
        {{ cardDescription }}
      </div>
      <div class="card-power text-black font-bold">
        {{ cardPower }}/{{ cardToughness }}
      </div>
    </div>
  </div>
</template>

<script>
import redFrame from '@/assets/card-frames/red-frame.png'
import blueFrame from '@/assets/card-frames/blue-frame.png'
import blackFrame from '@/assets/card-frames/black-frame.png'
import greenFrame from '@/assets/card-frames/green-frame.png'
import whiteFrame from '@/assets/card-frames/white-frame.png'
import multicoloredFrame from '@/assets/card-frames/multicolored-frame.png'


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
    };
  },
  computed: {
    charCount() {
      return this.cardDescription.length;
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
    charCount(newCount) {
      if (newCount > 181) {
        this.fontSize = 9;
      } else {
        this.fontSize = 11;
      }
    },
  },
  created() {
    // Check the initial character count
    if (this.charCount > 181) {
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
}

.card-cost {
  position: absolute;
  top: 20px;
  right: 26px;
  font-size: 12px; /* you can adjust this as needed */
  /* border: solid red 1px; */
}

.card-type {
  /* border: solid red 1px; */
  position: absolute;
  top: 198px;
  left: 25px;
  font-size: 10px; /* you can adjust this as needed */
}

.card-description {
  /* border: solid red 1px; */
  position: absolute;
  top: 220px; /* this might be the middle of the card, adjust as needed */
  left: 22px;
  right: 24px; /* add some padding on the right side */
  bottom: 40px;
  font-size: 11px; /* adjust as needed */
}

.card-power {
  position: absolute;
  bottom: 16px;
  right: 28px;
  font-size: 16px; /* adjust as needed */
}
</style>