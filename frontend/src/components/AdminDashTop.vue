<script setup>
import { ref } from 'vue';
import { adminStore } from '../store';
import { computed } from '@vue/reactivity';

const style2 = computed(()=>{
    return adminStore.path==1 ? "nav-link active" :  "nav-link"
})
const style3 = computed(()=>{
    return adminStore.path==2 ? "nav-link active" :  "nav-link"
})

</script>
<template>
    <div class="container">
        <header class="d-flex justify-content-center py-3">
            <ul class="nav nav-pills">
                <li class="nav-item"><a href="#" @click="adminStore.path=1;adminStore.getCat();" :class=style2>Categories</a></li>
                <li class="nav-item"><a href="#" @click="adminStore.path=2;adminStore.getApprovals();adminStore.getUnapproved()" :class=style3>Approvals Pending</a></li>
            </ul>
        </header>
    </div>
</template>
