<template id="registration-template">
    <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
        <div class="card shadow-sm p-4" style="width: 100%; max-width: 400px;">
            <h2 class="text-center mb-4">MasteQuiz : Register</h2>

            <form @submit.prevent="registerUser">
                <!-- Full Name Input -->
                <div class="mb-3">
                    <label for="full-name" class="form-label">Full Name</label>
                    <input id="full-name" v-model="fullName" type="text" class="form-control" required
                        placeholder="Full Name" />
                </div>

                <!-- Email Input -->
                <div class="mb-3">
                    <label for="email-address" class="form-label">Email address</label>
                    <input id="email-address" v-model="email" type="email" class="form-control" required
                        placeholder="Email address" />
                </div>

                <!-- Password Input -->
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input id="password" v-model="password" type="password" class="form-control" required
                        placeholder="Password" />
                </div>

                <!-- Login Link -->
                <div class="mb-3 d-flex justify-content-between">
                    <span class="text-secondary">Already have an account?
                        <router-link to="/login" class="text-primary text-decoration-none">Login</router-link>
                    </span>
                </div>

                <!-- Submit Button -->
                <button type="submit" class="btn btn-primary w-100">Register</button>

                <!-- Error Message -->
                <div v-if="errorMessage" class="text-center text-danger mt-3">
                    {{ errorMessage }}
                </div>
            </form>
        </div>
    </div>
</template>


<script>
export default {
    name: 'RegistrationComponent',
    data() {
        return {
            fullName: '',
            email: '',
            password: '',
            errorMessage: ''
        }
    },
    methods: {
        registerUser() {
            this.errorMessage = '';

            if (!this.fullName || !this.email || !this.password) {
                this.errorMessage = 'Please fill in all fields';
                return;
            }

            const registrationData = {
                full_name: this.fullName,
                email: this.email,
                password: this.password,
            };

            fetch('http://127.0.0.1:5000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(registrationData)
            })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            throw new Error(errorData.message || 'Registration failed');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    this.$router.push('/login');
                })
                .catch(error => {
                    this.errorMessage = error.message;
                });
        }
    }
}
</script>