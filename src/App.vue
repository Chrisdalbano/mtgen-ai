<template>
  <!-- <NavBar/> -->
  <router-view />
  <footer class="bg-gray-900 text-gray-200 p-4 font-beleren">
    <p class="text-center">
      Made with ❤️ by
      <a
        href="http://www.chrisdalbano.com"
        class="transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-110"
        target="_blank"
      >
        Chrisdalbano
      </a>
    </p>
    <p class="text-center"> {{ new Date().getFullYear() }} MTGen AI.</p>
    <p class="text-center text-sm opacity-50">
      All rights reserved, not afiliated with Wizards of the Coast, Magic The
      Gathering or any of their products.
    </p>
    
  </footer>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "App",
  components: { NavBar },
};
</script>
<style></style>
