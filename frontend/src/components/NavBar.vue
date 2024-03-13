<script setup>
import LoginContent from './LoginContent.vue';
import { userStore } from '../store';
import { customerStore } from '../store';
import CartContent from './CartContent.vue';
function exportcsv() {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${userStore.token}`
    },
    body: JSON.stringify({ "mail": userStore.id })
  };
  fetch('http://localhost:5000/productsummary', options)
    .then((response) => {
      if (response.status == 200) {
      }
    })
    .catch(err => { console.error(err) });
}
</script>
<template>
  <nav class="py-2 bg-light border-bottom">
    <div class="container d-flex flex-wrap justify-content-between form-inline">
      <span class="px-2 pt-2 h5">FreshFinds</span>
      <div class="form-group flex-grow-1 ms-5 me-3">
        <input v-model="customerStore.searchTerm" v-if="userStore.userType == 2" type="text" class="form-control"
          placeholder="Search items" />
      </div>
      <ul class="nav">
        <li class="nav-item">
          <div v-if="userStore.token" class="dropdown">
            <a class="btn dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-person-circle"></i> {{ userStore.id }}
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#" @click="userStore.logout()">Logout</a></li>
            </ul>
          </div>
          <button v-else type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#loginModal">
            Login
          </button>
        </li>
        <li class="nav-item">
          <button @click="exportcsv" v-if="userStore.userType == 1" type="button" class="btn btn-primary">
            Export
          </button>
        </li>
        <li v-if="userStore.userType == 2" class="nav-item">
          <button type="button" class="btn ms-2" data-bs-toggle="modal" data-bs-target="#cartModal">
            <i class="bi bi-cart-fill"></i> My Cart
          </button>
        </li>
      </ul>
    </div>
  </nav>
  <div data-bs-backdrop="static" class="modal fade modal-sheet p-4 py-md-5" id="loginModal" tabindex="-1" role="dialog"
    aria-labelledby="exampleModalLabel" aria-hidden="true">
    <LoginContent />
  </div>
  <div class="modal fade modal-sheet p-4 py-md-5" id="cartModal" tabindex="-1" role="dialog"
    aria-labelledby="exampleModalLabel" aria-hidden="true">
    <CartContent />
  </div>
</template>
