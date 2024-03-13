<script setup>
import { managerStore } from '../store';
const props = defineProps({
  name: String,
  cost: Number,
  expiry: String,
  size: String,
  id: Number,
  imgid: Number,
  units: Number,
})

defineEmits(['edit', 'delete'])

function imgurl() {
  return `http://localhost:5000/image/${props.imgid}`
}
</script>
<template>
  <div class="card me-3 mb-3 p-0 border" style="width: 12rem; height: 18rem;">
    <span class="position-absolute m-2 badge rounded-pill bg-primary">
      {{ props.expiry }}
    </span>
    <div class="card-body p-5">
      <h4 class="card-title p-0 m-0 ms-1">{{ props.name }}</h4>
      <p class="card-text p-0 m-1">
      <div class="d-flex">
        <div class="flex-fill">
          <div class="text-secondary">
            {{ props.size }}
          </div>
          &#8377;{{ props.cost }}
          <div>
            Units : {{ props.units }}
          </div>
        </div>
        <div>
          <button @click="$emit('edit')" data-bs-toggle="modal" data-bs-target="#ProdEditModal"
            class="btn btn-link m-0 p-0 me-2">
            Edit
          </button>
          <button data-bs-toggle="modal" data-bs-target="#ProdDeleteModal" @click="$emit('delete')"
            class="btn btn-link m-0 p-0">
            Delete
          </button>
        </div>
      </div>
      </p>
    </div>
  </div>
</template>
