<script setup>
import { ref, onMounted } from 'vue';
import { customerStore } from '../store';

const Categories = ref([])

onMounted(() => {
  getCategories()
})

function getCategories() {
  fetch("http://localhost:5000/categories", {
    method: "GET",
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return Promise.reject(response);
    })
    .then((json) => {
      Categories.value = json
      if (Categories.value.length > 0) {
        customerStore.currentCategory = Categories.value[0].id
      }
    })
    .catch(() => {
      Categories.value = []
      customerStore.currentCategory = -1
    });
}

function style(n) {
  return customerStore.currentCategory == n ? "nav-link active d-flex" : "nav-link link-body-emphasis d-flex"
}

</script>
<template>
  <div class="d-flex flex-column flex-shrink-0 p-3" style="width: 240px;">
    <a class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none">
      <span class="fs-4 ms-2 ps-1">Categories</span>
    </a>
    <hr>
    <ul class="nav nav-pills flex-column mb-auto">
      <li v-for="c in Categories" class="nav-item">
        <a href="#" @click="customerStore.currentCategory=c.id" :class="style(c.id)" aria-current="page">
          {{ c.name }}
        </a>
      </li>
    </ul>
  </div>
</template>
