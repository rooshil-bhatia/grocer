<script setup>
import { ref } from 'vue';
import { adminStore } from '../store';

const CloseEditCategory = ref(null);

async function send() {
    await adminStore.editCat()
        .then((result) => {
            if (result) {
                adminStore.getCat()
                CloseEditCategory.value.click()
                adminStore.catName = ""
                adminStore.catDescription = ""
            }
        })
}

</script>
<template>
    <div class="modal-dialog" role="document">
        <div class="modal-content rounded-4 shadow">
            <div class="modal-header p-5 pb-4 border-bottom-0">
                <h1 class="fw-bold mb-0 fs-2">Edit category</h1>
                <button type="button" ref="CloseEditCategory" class="btn-close" data-bs-dismiss="modal"
                    aria-label="Close"></button>
            </div>

            <div class="modal-body p-5 pt-0">
                <form class="" onsubmit="return false">
                    <div class="form-floating mb-3">
                        <input v-model="adminStore.catName" type="text" class="form-control rounded-3" id="floatingInput">
                        <label for="floatingInput">Category Name</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="text" v-model="adminStore.catDescription" class="form-control rounded-3" id="floatingPassword">
                        <label for="floatingPassword">Description</label>
                    </div>
                    <button @click="send" class="w-100 mb-2 btn btn-lg rounded-3 btn-primary">Edit</button>
                </form>
            </div>
        </div>
    </div>
</template>