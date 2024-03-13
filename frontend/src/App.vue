<script setup>
import { RouterLink, RouterView } from "vue-router";
import { userStore } from "./store";
import NavBar from "./components/NavBar.vue";
</script>

<template>
  <NavBar />
  <RouterView />  
</template>
