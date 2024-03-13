import { reactive, watch, ref } from "vue";
import router from './router'


export const userStore = reactive({
    token: '',
    id: '',
    userType: 2,
    approved: -1,
    async login(mail_, password_) {
        const data = { mail: mail_, password: password_ };
        await fetch("http://localhost:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.token = json["access_token"];
                this.id = mail_;
                this.userType = json["role"];
                this.approved = json["approved"];
            })
            .catch(() => {
                this.access_token = "";
            });
    },
    async signup(mail_, password_, role_) {
        const data = { mail: mail_, password: password_, role: role_ };
        await fetch("http://localhost:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.token = json["access_token"];
                this.id = mail_;
                this.userType = json["role"];
                this.approved = json["approved"];
            })
            .catch(() => {
                this.access_token = "";
            });
    },
    logout() {
        this.token = ''
        this.id = ''
        this.userType = 2
        this.approved = -1
    }
})

watch(
    () => userStore.userType,
    (type) => {
        if (type == 0) {
            router.push('/admin')
        }
        else if (type == 1) {
            router.push('/manager')
        }
        else {
            router.push('/')
        }
    }
)

export const adminStore = reactive({
    path: 1,
    dialogType: 0,
    catName: '',
    catDescription: '',
    catID: 0,
    catergories: [],
    managers_unapproved: [],
    requests_cat: [],
    async getCat() {
        await fetch("http://localhost:5000/categories", {
            method: "GET",
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.catergories = json
            })
            .catch(() => {
                this.catergories = []
            });
    },
    async newCat() {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "name": this.catName, "description": this.catDescription })
        };
        let status = false
        await fetch('http://localhost:5000/categories', options)
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status;
    },
    async editCat() {
        const options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "id": this.catID, "name": this.catName, "description": this.catDescription })
        };
        let status = false
        await fetch('http://localhost:5000/categories', options)
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status;
    },
    async delCat() {
        const options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "id": this.catID })
        };
        let status = false
        await fetch('http://localhost:5000/categories', options)
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status;
    },
    async getUnapproved() {
        await fetch("http://localhost:5000/managers", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.managers_unapproved = json
            })
            .catch(() => {
                this.managers_unapproved = []
            });
    },
    async approve(n) {
        let status = false
        await fetch("http://localhost:5000/approve", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "id": n })
        })
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status
    },
    async reject(n) {
        let status = false
        await fetch("http://localhost:5000/declinemanager", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "id": n })
        })
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status
    },
    async getApprovals() {
        await fetch("http://localhost:5000/catapprovals", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.requests_cat = json
            })
            .catch(() => {
                this.requests_cat = []
            });
    },
    async approveCat(id) {
        let status = false
        await fetch("http://localhost:5000/catapprovals", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "id": id })
        })
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status
    },
    async declineCat(id) {
        let status = false
        await fetch("http://localhost:5000/catapprovals", {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "id": id })
        })
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status
    }
})

export const managerStore = reactive({
    cat: 0,
    catergories: [],
    dialogType: 0,
    catName: '',
    catDescription: '',
    catID: 0,
    prodName: '',
    prodExpiry: '',
    prodRate: '',
    prodQuantity: '',
    prodID: 0,
    prods: [],
    async getCat() {
        await fetch("http://localhost:5000/categories", {
            method: "GET",
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.catergories = json
            })
            .catch(() => {
                this.catergories = []
            });
    },
    async delCat() {
        const options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "task": "-1", "name": this.catName, "description": this.catDescription, "cid": this.catID })
        };

        fetch('http://localhost:5000/catapprovals', options)
            .then(response => response.json())
            .then(response => console.log(response))
            .catch(err => console.error(err));
    },
    async editCat() {
        let status = false
        const options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "cid": this.catID, "name": this.catName, "description": this.catDescription, "task": 1 })
        };

        await fetch('http://localhost:5000/catapprovals', options)
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status;
    },
    async addCat() {
        let status = false;
        const options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userStore.token}`
            },
            body: JSON.stringify({ "name": this.catName, "description": this.catDescription, "task": 0 })
        };

        await fetch('http://localhost:5000/catapprovals', options)
            .then((response) => {
                if (response.status == 200) {
                    status = true
                }
            })
            .catch(err => { console.error(err) });
        return status;
    },
    async getProd() {
        await fetch(`http://localhost:5000/products/${this.cat}`, {
            method: "GET",
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.prods = json
            })
            .catch(() => {
                this.prods = []
            });
    },
})

export const customerStore = reactive({
    currentCategory: -1,
    products: [],
    cart: {},
    searchTerm: '',
    total: 0,
    async getProducts() {
        await fetch(`http://localhost:5000/products/${this.currentCategory}`, {
            method: "GET",
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                return Promise.reject(response);
            })
            .then((json) => {
                this.products = json
            })
            .catch(() => {
                this.products = []
            });
    },
})

watch(
    () => customerStore.currentCategory,
    (cat) => {
        if (cat != -1) {
            customerStore.getProducts()
        }
    }
)