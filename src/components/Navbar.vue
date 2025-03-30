<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">MasterQuiz : Admin Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <button class="btn btn-outline-light btn-danger" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'Navbar',
    methods: {
      logout() {
        // Implement logout logic
        localStorage.removeItem('admin_token')
        localStorage.removeItem('role')
        this.$router.push('/login')
      }
    }
  }
  </script>