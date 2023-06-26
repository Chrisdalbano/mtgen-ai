<template>
  <NavBar/>
  <router-view/>
  <footer></footer>
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
