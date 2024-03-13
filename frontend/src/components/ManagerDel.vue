<script setup>
import { managerStore } from '../store';

async function del() {
    await managerStore.delCat()
        .then((result) => {
            if (result) {
                managerStore.getCat()
            }
        })
}

</script>
<template>
    <div class="modal-dialog" role="document">
        <div class="modal-content rounded-3 shadow">
            <div class="modal-body p-4 text-center">
                <h5 class="mb-0">Delete category : {{ managerStore.catName }}?</h5>
            </div>
            <div class="modal-footer flex-nowrap p-0">
                <button type="button" @click="del"
                    class="btn btn-lg btn-link fs-6 text-decoration-none col-6 py-3 m-0 rounded-0 border-end"
                    data-bs-dismiss="modal"><strong>Yes</strong></button>
                <button type="button" class="btn btn-lg btn-link fs-6 text-decoration-none col-6 py-3 m-0 rounded-0"
                    data-bs-dismiss="modal">No</button>
            </div>
        </div>
    </div>
</template>