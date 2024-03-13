<script setup>
import { adminStore } from '../store';
const props = defineProps({
  name: String,
  description: String,
  id: Number,
})
function setEdit(){
    const n = props.id
    adminStore.dialogType = 1
    adminStore.catID = n
    adminStore.catName = props.name
    adminStore.catDescription = props.description
}

function setDel(){
    const n = props.id
    adminStore.dialogType = 2
    adminStore.catID = n
    adminStore.catName = props.name
}

</script>
<template>
    <div class="col d-flex align-items-start">
        <div>
            <h3 class="fw-bold mb-0 fs-4 text-body-emphasis">{{name}}</h3>
            <p>{{ description }}</p>
            <button @click="setEdit()" data-bs-toggle="modal" data-bs-target="#CatModal" type="button" class="m-0 p-0 btn btn-link">Edit</button>
            <button @click="setDel()" data-bs-toggle="modal" data-bs-target="#CatModal"  type="button" class="m-0 p-0 ps-4 btn btn-link">Delete</button>
        </div>
    </div>
</template>