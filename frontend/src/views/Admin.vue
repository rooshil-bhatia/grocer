<script setup>
import { ref } from "vue";
import AdminDashTop from "../components/AdminDashTop.vue";
import CategoryList from "../components/CategoryList.vue";
import Approvals from "../components/Approvals.vue";
import { adminStore } from "../store";
</script>
<template>
    <AdminDashTop />
    <CategoryList v-if="adminStore.path==1"/>
    <Approvals v-else />
</template>