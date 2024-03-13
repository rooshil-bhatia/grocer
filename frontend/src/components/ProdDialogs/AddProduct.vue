<script setup>
import { ref } from 'vue';
import { managerStore, userStore } from '../../store';

const CloseProdAddDiag = ref(null);

const name = ref('')
const expiry = ref('')
const rate = ref(null)
const quantity = ref('')
const units = ref(null)

const props = defineProps(['categoryid'])

const success = ref(0)

const url = ref('')

// const props = defineProps(['name','expiry','rate','quantity','id'])

function close() {
    success.value = 0
    CloseProdAddDiag.value.click()
}



function add() {
    const formData = new FormData();
    formData.append('json', JSON.stringify({ "name": name.value, "expiry": expiry.value, "rate": rate.value, "quantity": quantity.value, "cid": props.categoryid, "units": units.value }));
    const options = {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${userStore.token}`
        },
        body: formData
    };
    fetch('http://localhost:5000/products', options)
        .then((response) => {
            name.value = ""
            expiry.value = ""
            rate.value = 0
            quantity.value = ""
            if (response.status == 200) {
                success.value = 1
                setTimeout(close, 300)
                managerStore.getProd()
            }
            else {
                success.value = -1
            }
        })
}

</script>
<template>
    <div class="modal-dialog" role="document">
        <div class="modal-content rounded-4 shadow">
            <div class="modal-header p-5 pb-4 border-bottom-0">
                <h1 class="fw-bold mb-0 fs-2">Add new product</h1>
                <button type="button" ref="CloseProdAddDiag" class="btn-close" data-bs-dismiss="modal"
                    aria-label="Close"></button>
            </div>

            <div class="modal-body p-5 pt-0">
                <form class="" onsubmit="return false">
                    <div class="form-floating mb-3">
                        <input v-model="name" type="text" class="form-control rounded-3" id="prodName">
                        <label for="prodName">Product Name</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="expiry" type="date" class="form-control rounded-3" id="prodExpiry">
                        <label for="prodExpiry">Expiry</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="rate" type="number" class="form-control rounded-3" id="prodRate">
                        <label for="prodRate">Rate</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="units" type="number" class="form-control rounded-3" id="units">
                        <label for="units">Units</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="quantity" type="text" class="form-control rounded-3" id="prodQuantity">
                        <label for="prodQuantity">Quantity</label>
                    </div>
                    <div class="alert alert-success" role="alert" v-if="success == 1">
                        Product added
                    </div>
                    <div class="alert alert-success" role="alert" v-if="success == -1">
                        Failed to add product
                    </div>
                    <button @click="add" class="w-100 mb-2 btn btn-lg rounded-3 btn-primary">Add</button>
                </form>
            </div>
        </div>
    </div>
</template>