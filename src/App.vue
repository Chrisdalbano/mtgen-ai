<template>
  <NavBar/>
  <router-view/>
  <footer>Footer</footer>
</template>



<script>
import NavBar from "@/components/NavBar.vue"

export default {
  name: "App",
  components: { NavBar },
}
</script>
<style>


</style>
