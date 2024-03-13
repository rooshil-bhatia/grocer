<script setup>
import { ref } from 'vue';


const mail_login = ref('')
const pass_login = ref('')

const mail_register = ref('')
const pass_register = ref('')

</script>

<template>
  <div class="container d-flex mt-5">
    <div class="container flex-fill border-end me-2">
      <span class="h2">Login</span>
      <div class="input-group mt-5">
        <span class="input-group-text" id="mail">@</span>
        <input
          type="text"
          class="form-control"
          placeholder="E-mail ID"
          aria-label="Mail"
          aria-describedby="mail"
        />
      </div>
      <div class="input-group mt-4">
        <input type="password" class="form-control" placeholder="Password" />
      </div>
      <button type="button" class="btn btn-primary mt-5">Sign in</button>
    </div>
    <div class="container flex-fill ms-2">
      <span class="h2">Register</span>
      <div class="input-group mt-5">
        <span class="input-group-text" id="mail">@</span>
        <input
          type="text"
          class="form-control"
          placeholder="E-mail ID"
          aria-label="Mail"
          aria-describedby="mail"
        />
      </div>
      <div class="input-group mt-4">
        <input type="password" class="form-control" placeholder="Password" />
      </div>
      <div class="form-check form-check-inline mt-4">
        <input
          class="form-check-input"
          type="radio"
          id="inlineCheckbox1"
          value="option1"
          name="role"
        />
        <label class="form-check-label" for="inlineCheckbox1">Customer</label>
      </div>
      <div class="form-check form-check-inline mt-4">
        <input
          class="form-check-input"
          type="radio"
          id="inlineCheckbox2"
          value="option2"
          name="role"
        />
        <label class="form-check-label" for="inlineCheckbox2"
          >Store Manager</label
        >
      </div>
      <div></div>
      <button type="button" class="btn btn-primary mt-4">Register</button>
    </div>
  </div>
</template>
