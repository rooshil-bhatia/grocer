<script setup>
import Category from "../components/Catergory.vue";
import ItemCard from "../components/ItemCard.vue";
import { customerStore } from "../store";
import { computed } from "@vue/reactivity";
const filtered = computed(() => {
  return customerStore.products.filter(function (v) {
        return v.name.toUpperCase().includes(customerStore.searchTerm.toUpperCase());
    });
})
</script>

<template>
  <main>
    <div class="container d-flex">
      <Category />
      
      <div class="container p-3">
        <p v-if="customerStore.searchTerm" class="h4 pb-4">Showing results for "{{ customerStore.searchTerm }}"</p>
        <!-- <Crumb /> -->
        <div class="container">
          <div class="row row-cols-auto">
            <ItemCard v-for="p in filtered" :name="p.name"
              img-url="https://thumbs.dreamstime.com/b/red-tomato-23480454.jpg" :size="p.quantity" :cost="p.rate"
              :expiry="p.expiry" :id="p.id" :imgid="p.imgid" :units="p.units" />
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
