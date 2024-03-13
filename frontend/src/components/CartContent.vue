<script setup>
import { computed, ref } from '@vue/reactivity';
import { customerStore, userStore } from '../store';
import CartItem from './CartItem.vue';
const realTotal = computed(() => {
    return customerStore.total > 1200 ? customerStore.total - 200 : customerStore.total
})

const success = ref(0)

async function order() {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${userStore.token}`
        },
        body: JSON.stringify({'mail':userStore.id,'order':JSON.stringify(customerStore.cart)})
    };
    await fetch('http://localhost:5000/orders', options)
        .then((response) => {
            if (response.status == 200) {
                success.value = 1
            }
        })
        .catch(success.value = -1);
}
</script>
<template>
    <div class="modal-dialog" role="document">
        <div class="modal-content rounded-4 shadow">
            <div class="modal-header p-4 pb-2 border-bottom-0">
                <h1 class="fw-bold mb-0 fs-2">Your cart</h1>
                <button type="button" ref="Close" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="order-md-last pt-4 ps-3 pe-3 pb-4">
                <ul class="list-group mb-3">
                    <li v-for="(value, key) in customerStore.cart" :key="key"
                        class="list-group-item d-flex justify-content-between lh-sm">
                        <CartItem :id="key" :quantity="value" />
                    </li>
                    <li v-if="customerStore.total > 1200"
                        class="list-group-item d-flex justify-content-between bg-body-tertiary">
                        <div class="text-success">
                            <h6 class="my-0">Promo code</h6>
                            <small>SALE200</small>
                        </div>
                        <span class="text-success">−200</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        <span>Total (Rs)</span>
                        <strong>{{ realTotal }}</strong>
                    </li>
                </ul>
                <div v-if="success == 1" class="alert alert-success mt-3" role="alert">
                    Order placed!
                </div>
                <div v-else-if="success == -1" class="alert alert-danger mt-3" role="alert">
                    Failed to place order
                </div>
                <div class="d-grid gap-2">
                    <button @click="order()" class="btn btn-primary" type="button">Order</button>
                </div>
            </div>
        </div>
    </div>
</template>