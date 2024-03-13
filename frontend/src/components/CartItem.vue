<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps(['id', 'quantity'])
const name = ref('')
const rate = ref(0)
onMounted(() => {
    fetch(`http://localhost:5000/product/${props.id}`, {
        method: "GET",
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            }
            return Promise.reject(response);
        })
        .then((json) => {
            name.value = json['name'];
            rate.value = json['rate'];
        })
        .catch(() => {
        });
})
</script>
<template>
    <div>
        <h6 class="my-0">{{ name }}</h6>
        <small class="text-body-secondary">{{ rate }}</small>
    </div>
    <span class="text-body-secondary">{{ quantity }}</span>
    <span class="text-body-secondary">{{ rate * quantity }}</span>
</template>