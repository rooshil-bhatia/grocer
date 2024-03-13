<script setup>
import ManagerDash from '../components/ManagerDash.vue';
import { userStore } from '../store';
</script>
<template>
    <ManagerDash v-if="userStore.approved"/>
    <div v-else>
        Manager not approved yet
    </div>
</template>