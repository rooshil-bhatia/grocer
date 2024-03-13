<script setup>
import { ref } from 'vue'
import { userStore } from '../store';
const loginFlag = ref(true);

const mail = ref('');
const password = ref('');
const role = ref(2);

const Close = ref(null);

function loginSwitch() {
    loginFlag.value = !loginFlag.value;
}

async function login_() {
    await userStore.login(mail.value, password.value);
    if (userStore.token) {
        Close.value.click();
    }
}

async function signup_() {
    await userStore.signup(mail.value, password.value, role.value);
    if (userStore.token) {
        Close.value.click();
    }
}

</script>
<template>
    <div class="modal-dialog" role="document">
        <div class="modal-content rounded-4 shadow">
            <div class="modal-header p-5 pb-4 border-bottom-0">
                <h1 v-if="loginFlag" class="fw-bold mb-0 fs-2">Sign in</h1>
                <h1 v-else class="fw-bold mb-0 fs-2">Sign up</h1>
                <button type="button" ref="Close" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <div class="modal-body p-5 pt-0">
                <form class="" onsubmit="return false">
                    <div class="form-floating mb-3">
                        <input v-model="mail" type="text" class="form-control rounded-3" id="floatingInput"
                            placeholder="name@example.com">
                        <label for="floatingInput">Email address</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="password" type="password" class="form-control rounded-3" id="floatingPassword"
                            placeholder="Password">
                        <label for="floatingPassword">Password</label>
                    </div>
                    <div v-if="!loginFlag">
                        <fieldset>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" id="contactChoice2" name="role" value="2" v-model="role"/>
                                <label class="form-check-label" for="contactChoice2"> Customer</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" id="contactChoice1" name="role" value="1" v-model="role"/>
                                <label class="form-check-label" for="contactChoice1"> Manager</label>
                            </div>
                        </fieldset>
                    </div>
                    <div class="my-3">
                        <a href="#" @click="loginSwitch" v-if="loginFlag" class="link-opacity-100 text-primary"><u>New user?
                                Register
                                here</u></a>
                        <a href="#" @click="loginSwitch" v-if="!loginFlag" class="link-opacity-100 text-primary"><u>Have an
                                account? Sign
                                in</u></a>
                    </div>
                    <button v-if="loginFlag" @click="login_" class="w-100 mb-2 btn btn-lg rounded-3 btn-primary">Sign
                        in</button>
                    <button v-else @click="signup_" class="w-100 mb-2 btn btn-lg rounded-3 btn-primary">Sign up</button>
                    <small v-if="!loginFlag" class="text-body-secondary">By clicking Sign up, you agree to the terms of
                        use.</small>
                </form>
            </div>
        </div>
    </div>
</template>
