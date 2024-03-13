<script setup>
import { customerStore } from "../store";
const props = defineProps({
  name: String,
  cost: Number,
  expiry: String,
  size: String,
  id: Number,
  imgid:Number,
  units: Number,
})

function outofstock(){
  if(props.units<1) return true
  else
    return false
}

function add() {
  if (props.id in customerStore.cart)
    {
      if(props.units>customerStore.cart[props.id])
        customerStore.cart[props.id]++
    }
  else
    customerStore.cart[props.id] = 1
  customerStore.total+=props.cost
}

function remove() {
  if (customerStore.cart[props.id]>1)
    customerStore.cart[props.id]--
  else
    delete customerStore.cart[props.id]
  customerStore.total-=props.cost
}

function getImg(){
  return `http://localhost:5000/image/${props.imgid}`
}

</script>
<template>
  <div class="card me-3 mb-3 p-0 border" style="width: 12rem; height: 18rem;">
    <span class="position-absolute m-2 badge rounded-pill bg-primary">
      {{ props.expiry }}
    </span>

    <div class="card-body p-5">

      <div class="mb-3">
      <div>
        <h3 class="card-title">{{ props.name }}</h3>
      </div>
        <div class="text-secondary mb-2">
          {{ props.size }}
        </div>
        <div>
          &#8377;{{ props.cost }}
        </div>
      </div>

      <div>
        <div v-if="outofstock()" class="text-danger">
          Out of stock
        </div>
        <div v-else-if="props.id in customerStore.cart && customerStore.cart[props.id]" class="btn-group" role="group" aria-label="Basic outlined example">
          <button @click="remove" type="button" class="btn btn-outline-primary">-</button>
          <button type="button" class="btn btn-outline-primary">{{ props.id in customerStore.cart ? customerStore.cart[props.id] : 0 }}</button>
          <button @click="add" type="button" class="btn btn-outline-primary">+</button>
        </div>
        <button v-else @click="add" class="btn btn-success">
          Add
        </button>
      </div>

    </div>
  </div>
</template>

