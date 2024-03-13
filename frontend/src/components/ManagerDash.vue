<script setup>
import { onMounted, ref } from 'vue';
import { managerStore } from '../store';
import ManCatAdd from './ManCatAdd.vue';
import ManagerEdit from './ManagerEdit.vue';
import ManagerDel from './ManagerDel.vue';
import AddProduct from './ProdDialogs/AddProduct.vue';
import ManagerCard from './ManagerCard.vue'
import EditProduct from './ProdDialogs/EditProduct.vue';
import DelProduct from './ProdDialogs/DelProduct.vue';
function style(n) {
    return managerStore.cat == n ? "nav-link active d-flex" : "nav-link link-body-emphasis d-flex"
}

function setCat(n) {
    managerStore.cat = n;
    managerStore.getProd()
}

onMounted(() => {
    managerStore.getCat()
})

function setDel(n, name) {
    managerStore.dialogType = 2
    managerStore.catID = n
    managerStore.catName = name
}
function setEdit(n, name, description) {
    managerStore.dialogType = 1
    managerStore.catID = n
    managerStore.catName = name
    managerStore.catDescription = description
}
function setValues(name, rate, expiry, quantity, id,units) {
    prodid.value = id
    pname.value = name
    prate.value = rate
    pexpiry.value = expiry
    pquantity.value = quantity
    pcatID.value = managerStore.cat
    punits.value = units
}

const pname = ref('')
const prate = ref(0)
const pexpiry = ref('')
const pquantity = ref('')
const prodid = ref(0)
const pcatID = ref(-1)
const punits = ref(0)
</script>
<template>
    <div class="container mt-2 d-flex">
        <div class="d-flex flex-column flex-shrink-0 p-3" style="width: 240px;">
            <a class="d-flex mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none">
                <span class="fs-4 ms-2 ps-1 flex-fill">Categories</span>
                <button @click="addCategory" data-bs-toggle="modal" data-bs-target="#ManCatModal" type="button"
                    class="ms-2 p-0 btn btn-link">Add</button>
            </a>
            <hr>
            <ul class="nav nav-pills flex-column mb-auto">
                <li v-for="m in managerStore.catergories" :key="m.id" class="nav-item">
                    <a @click="setCat(m.id)" href="#" :class=style(m.id) aria-current="page">
                        <span class="flex-fill">{{ m.name }}</span>
                        <i @click="setEdit(m.id, m.name, m.description)" data-bs-toggle="modal"
                            data-bs-target="#ManCatModal" class="bi bi-pencil-square me-2"></i>
                        <i @click="setDel(m.id, m.name)" data-bs-toggle="modal" data-bs-target="#ManCatModal"
                            class="bi bi-trash"></i>
                    </a>
                </li>
            </ul>
        </div>
        <div class="m-3 me-md-auto link-body-emphasis text-decoration-none">
            <p><span class="fs-4 ps-1">Products</span></p>
            <button @click="setValues('', 0, '', '', 0)" v-if="managerStore.cat != 0" data-bs-toggle="modal"
                data-bs-target="#ProdAddModal" type="button" class="btn btn-outline-primary">Add</button>
            <div>
                <div class="row row-cols-auto pt-3">
                    <ManagerCard v-for="p in managerStore.prods" :name="p.name" :imgid="p.imgid" :size="p.quantity"
                        :expiry="p.expiry" :units="p.units" :cost="p.rate" :id="p.id" @edit="setValues(p.name, p.rate, p.expiry, p.quantity, p.id,p.units)"
                        @delete="setValues(p.name, 0, '', '', p.id)" />
                </div>
            </div>
        </div>
    </div>
    <div data-bs-backdrop="static" class="modal fade modal-sheet p-4 py-md-5" id="ManCatModal" tabindex="-1" role="dialog"
        aria-labelledby="exampleModalLabel" aria-hidden="true">
        <ManCatAdd v-if="managerStore.dialogType == 0" />
        <ManagerEdit v-else-if="managerStore.dialogType == 1" />
        <ManagerDel v-else-if="managerStore.dialogType == 2" />
    </div>
    <div data-bs-backdrop="static" class="modal fade modal-sheet p-4 py-md-5" id="ProdAddModal" tabindex="-1" role="dialog"
        aria-labelledby="exampleModalLabel" aria-hidden="true">
        <AddProduct :categoryid="pcatID" />
    </div>
    <div data-bs-backdrop="static" class="modal fade modal-sheet p-4 py-md-5" id="ProdEditModal" tabindex="-1" role="dialog"
        aria-labelledby="exampleModalLabel" aria-hidden="true">
        <EditProduct :id="prodid" :expiry="pexpiry" :name="pname" :quantity="pquantity" :rate="prate"
            :categoryid="pcatID" :units="punits" />
    </div>
    <div data-bs-backdrop="static" class="modal fade modal-sheet p-4 py-md-5" id="ProdDeleteModal" tabindex="-1"
        role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <DelProduct :id="prodid" :name="pname" />
    </div>
</template>
