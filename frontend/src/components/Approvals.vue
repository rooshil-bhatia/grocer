<script setup>
import { onMounted } from 'vue';
import { adminStore } from '../store';

onMounted(() => {
    adminStore.getUnapproved();
    adminStore.getApprovals();
})

async function approve(n) {
    const status = await adminStore.approve(n)
    if (status) {
        adminStore.getUnapproved();
    }
}

async function decline(n) {
    const status = await adminStore.reject(n)
    if (status) {
        adminStore.getUnapproved();
    }
}

async function approveCat(n) {
    const status = await adminStore.approveCat(n)
    if (status) {
        adminStore.getApprovals();
    }
}

async function declineCat(n) {
    const status = await adminStore.declineCat(n)
    if (status) {
        adminStore.getApprovals();
    }
}

</script>
<template>
    <div class="container d-flex">
        <div class="p-2 flex-fill">
            <h4 class="p-1">Manager approvals</h4>
            <ul class="list-group">
                <li v-for="m in adminStore.managers_unapproved" class="list-group-item d-flex">
                    <span class="flex-fill">{{ m.mail }}</span>
                    <button @click="approve(m.id)" type="button" class="btn btn-link p-0 m-0 ms-2 me-2">Approve
                    </button>
                    <button @click="decline(m.id)" type="button" class="btn btn-link p-0 m-0 ms-2 me-2">Decline
                    </button>
                </li>
            </ul>
        </div>
        <div class="p-2 flex-fill">
            <h4 class="p-1">Category approvals</h4>
            <ul class="list-group">
                <li v-for="m in adminStore.requests_cat" class="list-group-item">
                    <div>
                        <span class="lead" v-if="m.task == 0">Create new category</span>

                        <span class="lead" v-if="m.task == 1">Edit category</span>

                        <span class="lead" v-if="m.task == -1">Delete category</span>
                    </div>
                    <div v-if="m.task != 1">
                        <p>Name : {{ m.name }}</p>
                        <p>Description : {{ m.description }}</p>
                    </div>
                    <div class="d-flex" v-else>
                        <div class="flex-fill">
                            <h5>Old</h5>
                            <p>Name : {{ m.name }}</p>
                            <p>Description : {{ m.description }}</p>
                        </div>
                        <div class="flex-fill">
                            <h5>New</h5>
                            <p>Name : {{ m.oldname }}</p>
                            <p>Description : {{ m.olddesc }}</p>
                        </div>
                    </div>
                    <button @click="approveCat(m.id)" type="button" class="btn btn-link p-0 m-0 me-2">Approve
                    </button>
                    <button @click="declineCat(m.id)" type="button" class="btn btn-link p-0 m-0">Decline
                    </button>
                </li>
            </ul>
        </div>

    </div>
</template>