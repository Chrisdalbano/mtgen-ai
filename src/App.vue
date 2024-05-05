<template>
  <!-- <NavBar/> -->
  <router-view />
  <FooterComponent/>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import FooterComponent from "@/components/FooterComponent.vue"

export default {
  name: "App",
  components: { NavBar, FooterComponent },
};
</script>
<style></style>
