<template>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">MasterQuiz : Dashboard</a>
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
    <div class="student-dashboard py-5 bg-light" style="overflow: auto; max-height: 95vh">
  
      <!-- Search Input -->
      <div class="mb-4 container">
        <input v-model="searchQuery" type="text" class="form-control" placeholder="Search quizzes by course, chapter, date or remarks" />
      </div>
  
      <div class="container-fluid">
        <div class="row g-4">
          <!-- Available Quizzes Section -->
          <div class="col-md-6 col-lg-6">
            <div class="card shadow-sm">
              <div class="card-body">
                <h3 class="card-title mb-4">Available Quizzes</h3>
  
                <div v-if="loading" class="text-center">
                  <p>Loading quizzes...</p>
                </div>
  
                <div v-else-if="filteredQuizzes.length === 0" class="text-center text-secondary">
                  No quizzes available
                </div>
  
                <div v-else>
                  <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="mb-3 p-3 border rounded bg-light">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h5>{{ quiz.course_name }} - {{ quiz.chapter_name }}</h5>
                        <p class="mb-1 text-muted">Date: {{ formatDate(quiz.date_of_quiz) }} &nbsp;&nbsp;&nbsp;&nbsp; Duration: {{ quiz.time_duration }}</p>
                        <p class="mb-1 text-muted">Quiz Remark: {{ quiz.remarks }}</p>
                      </div>
                      <button class="btn btn-primary" @click="takeQuiz(quiz.id)">Take Quiz</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Quiz History Section -->
          <div class="col-md-6 col-lg-6">
            <div class="card shadow-sm">
              <div class="card-body">
                <h3 class="card-title mb-4">Quiz History</h3>
  
                <div v-if="loadingHistory" class="text-center">
                  <p>Loading quiz history...</p>
                </div>
  
                <div v-else-if="filteredHistory.length === 0" class="text-center text-secondary">
                  No quiz history found
                </div>
  
                <div v-else>
                  <div v-for="history in filteredHistory" :key="history.quiz_id" class="mb-3 p-3 border rounded bg-light">
                    <h5>{{ history.course_name }} - {{ history.chapter_name }}</h5>
                    <p class="mb-1 text-muted">Attempt Date: {{ formatDateTime(history.attempt_time) }}</p>
                    <p class="mb-0">
                      Score: <span :class="{
                        'text-success': history.score_percentage >= 70,
                        'text-warning': history.score_percentage >= 50 && history.score_percentage < 70,
                        'text-danger': history.score_percentage < 50
                      }">
                        {{ history.score_percentage.toFixed(2) }}%
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>  

<script>
export default {
    data() {
        return {
            quizzes: [],
            quizHistory: [],
            loading: false,
            loadingHistory: false,
            searchQuery: ''
        }
    },
    computed: {
        filteredQuizzes() {
            if (!this.searchQuery) return this.quizzes;

            const query = this.searchQuery.toLowerCase();
            return this.quizzes.filter(quiz =>
                quiz.course_name.toLowerCase().includes(query) ||
                quiz.chapter_name.toLowerCase().includes(query) ||
                quiz.remarks.toLowerCase().includes(query) ||
                quiz.date_of_quiz.toLowerCase().includes(query)
            );
        },
        filteredHistory() {
            if (!this.searchQuery) return this.quizHistory;

            const query = this.searchQuery.toLowerCase();
            return this.quizHistory.filter(history =>
                history.course_name.toLowerCase().includes(query) ||
                history.chapter_name.toLowerCase().includes(query)
            );
        }
    },
    mounted() {
        this.fetchQuizzes();
        this.fetchQuizHistory();
    },
    methods: {
        fetchQuizzes() {
            this.loading = true;
            const studentToken = localStorage.getItem('student_token');

            fetch('http://127.0.0.1:5000/student/quizzes', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${studentToken}`,
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch quizzes');
                    }
                    return response.json();
                })
                .then(data => {
                    this.quizzes = data;
                    this.loading = false;
                })
                .catch(error => {
                    console.error('Error fetching quizzes:', error);
                    this.loading = false;
                });
        },
        fetchQuizHistory() {
            this.loadingHistory = true;
            const studentToken = localStorage.getItem('student_token');

            fetch('http://127.0.0.1:5000/student/quiz-history', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${studentToken}`,
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch quiz history');
                    }
                    return response.json();
                })
                .then(data => {
                    this.quizHistory = data;
                    this.loadingHistory = false;
                })
                .catch(error => {
                    console.error('Error fetching quiz history:', error);
                    this.loadingHistory = false;
                });
        },
        logout() {
            // Implement logout logic
            localStorage.removeItem('student_token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        },
        takeQuiz(quizId) {
            // Navigate to the quiz page or open quiz modal
            this.$router.push(`/student/take-quiz/${quizId}`);
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString();
        },
        formatDateTime(dateTimeString) {
            return new Date(dateTimeString).toLocaleString();
        }
    }
}
</script>
