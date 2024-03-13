<script setup>
import { adminStore } from '../store.js';
import CategoryItem from '../components/CategoryItem.vue';
import CategoryDialog from "../components/CategoryDialog.vue";
import EditCategory from "../components/EditCategory.vue"
import DelCategory from './DelCategory.vue';
import { onMounted } from 'vue'

onMounted(() => {
    adminStore.getCat()
})
</script>
<template>
    <button @click="adminStore.dialogType = 0" data-bs-toggle="modal" data-bs-target="#CatModal" type="button"
        class="ms-4 me-3 btn btn-success"><i class="bi bi-plus-circle"></i> Add Category</button>
    <div class="ms-4 me-3 row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5">
        <CategoryItem v-for="cat in adminStore.catergories" :key="cat.id" :id="cat.id" :name="cat.name"
            :description="cat.desc" />
    </div>
    <div data-bs-backdrop="static" class="modal fade modal-sheet p-4 py-md-5" id="CatModal" tabindex="-1" role="dialog"
        aria-labelledby="exampleModalLabel" aria-hidden="true">
        <CategoryDialog v-if="adminStore.dialogType == 0" />
        <EditCategory v-else-if="adminStore.dialogType == 1" />
        <DelCategory v-else />
    </div>
</template>