<!-- Login Component -->
<template id="login-template">
    <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
        <div class="card shadow-sm p-4" style="width: 100%; max-width: 400px;">
            <h2 class="text-center mb-4">MasteQuiz : Login</h2>

            <form @submit.prevent="loginUser">
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

                <!-- Register Link -->
                <div class="mb-3 d-flex justify-content-between">
                    <span class="text-secondary">Don't have an account?
                        <router-link to="/register" class="text-primary text-decoration-none">Register</router-link>
                    </span>
                </div>

                <!-- Submit Button -->
                <button type="submit" class="btn btn-primary w-100">Sign In</button>

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
    name: 'LoginComponent',
    data() {
        return {
            email: '',
            password: '',
            errorMessage: ''
        }
    },
    methods: {
        loginUser() {
            // Reset error message
            this.errorMessage = '';

            // Basic client-side validation
            if (!this.email || !this.password) {
                this.errorMessage = 'Please enter email and password';
                return;
            }

            // Prepare login data
            const loginData = {
                email: this.email,
                password: this.password
            };

            // Send login request
            fetch('http://127.0.0.1:5000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            throw new Error(errorData.message || 'Login failed');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    // Successful login
                    // Store token and user info
                    localStorage.setItem('role', data.user.role);
                    if (data.user.role === 'admin') {
                        localStorage.setItem('admin_token', data.access_token);
                        this.$router.push('/master-dashboard');
                    } else {
                        localStorage.setItem('student_token', data.access_token);
                        this.$router.push('/student-dashboard');
                    }
                })
                .catch(error => {
                    // Handle login error
                    this.errorMessage = error.message;
                });
        }
    }
}
</script>