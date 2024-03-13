<script setup>
import { ref,watch } from 'vue';
import { managerStore, userStore } from '../../store';

const CloseProdAddDiag = ref(null);

const props = defineProps(['name','expiry','rate','quantity','categoryid','id','units'])
const pname = ref('')
const pexpiry = ref('')
const prate = ref(null)
const pquantity = ref('')
const success = ref(0)
const units = ref(0)


function close() {
    success.value = 0
    CloseProdAddDiag.value.click()
}


watch(props,(newProp)=>{
    pname.value = newProp.name
    pexpiry.value = newProp.expiry
    prate.value = newProp.rate
    pquantity.value = newProp.quantity
    units.value = newProp.units
})

function edit() {
    const formData = new FormData();
    formData.append('json', JSON.stringify({ "id":props.id, "name": pname.value, "expiry": pexpiry.value, "rate": prate.value, "quantity": pquantity.value, "cid": props.categoryid, "units": units.value }));
    const options = {
        method: 'PUT',
        headers: {
            Authorization: `Bearer ${userStore.token}`
        },
        body: formData
    };
    fetch('http://localhost:5000/products', options)
        .then((response) => {
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
                <h1 class="fw-bold mb-0 fs-2">Edit product</h1>
                <button type="button" ref="CloseProdAddDiag" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <div class="modal-body p-5 pt-0">
                <form class="" onsubmit="return false">
                    <div class="form-floating mb-3">
                        <input v-model="pname" type="text" class="form-control rounded-3" id="prodName">
                        <label for="prodName">Product Name</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="pexpiry" type="date" class="form-control rounded-3" id="prodExpiry">
                        <label for="prodExpiry">Expiry</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="prate" type="number" class="form-control rounded-3" id="prodRate">
                        <label for="prodRate">Rate</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="units" type="number" class="form-control rounded-3" id="units">
                        <label for="units">Units</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="pquantity" type="text" class="form-control rounded-3" id="prodQuantity">
                        <label for="prodQuantity">Quantity</label>
                    </div>
                    <div class="alert alert-success" role="alert" v-if="success==1">
                        Product edited
                    </div>
                    <div class="alert alert-success" role="alert" v-if="success==-1">
                        Failed to edit product
                    </div>
                    <button @click="edit" class="w-100 mb-2 btn btn-lg rounded-3 btn-primary">Edit</button>
                </form>
            </div>
        </div>
    </div>
</template>