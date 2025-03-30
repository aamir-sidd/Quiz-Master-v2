<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/student-dashboard">MasterQuiz : Quiz</router-link>
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
    <div class="container-fluid py-5 mb-5" style="overflow: auto; max-height: 95vh">
        <div v-if="loading" class="text-center text-primary fs-4">Loading quiz...</div>

        <div v-else-if="error" class="text-center text-danger">
            {{ error }}
        </div>

        <div v-else class="card shadow-sm p-4 mx-auto" style="max-width: 800px;">
            <div v-if="!quizSubmitted">
                <!-- Quiz Header -->
                <div class="mb-4 d-flex justify-content-between">
                    <h1 class="h4">Quiz</h1>
                    <div class="text-muted">Time Remaining: {{ formattedTimeRemaining }}</div>
                </div>

                <!-- Question Section -->
                <div v-if="currentQuestion" class="mb-4">
                    <h2 class="h5">{{ currentQuestion.question_statement }}</h2>

                    <div class="list-group mt-3">
                        <label v-for="(option, index) in [
                            currentQuestion.option1,
                            currentQuestion.option2,
                            currentQuestion.option3,
                            currentQuestion.option4
                        ]" :key="index" class="list-group-item list-group-item-action"
                            :class="{ 'active': selectedAnswers[currentQuestionIndex] === index + 1 }">
                            <input type="radio" :name="`question-${currentQuestion.id}`" :value="index + 1"
                                v-model="selectedAnswers[currentQuestionIndex]" class="me-2" />
                            {{ option }}
                        </label>
                    </div>
                </div>

                <!-- Navigation Buttons -->
                <div class="mt-4 d-flex justify-content-between">
                    <button v-if="currentQuestionIndex > 0" @click="previousQuestion"
                        class="btn btn-secondary">Previous</button>

                    <button v-if="currentQuestionIndex < questions.length - 1" @click="nextQuestion"
                        class="btn btn-primary ms-auto" :disabled="!selectedAnswers[currentQuestionIndex]">Next</button>

                    <button v-if="currentQuestionIndex === questions.length - 1" @click="submitQuiz"
                        class="btn btn-success ms-auto" :disabled="!selectedAnswers[currentQuestionIndex]">Submit
                        Quiz</button>
                </div>
            </div>

            <!-- Quiz Results Section -->
            <div v-else class="text-center">
                <h2 class="h4 mb-3">Quiz Results</h2>
                <div class="alert" :class="{
                    'alert-success': quizResult.score_percentage >= 70,
                    'alert-warning': quizResult.score_percentage >= 50 && quizResult.score_percentage < 70,
                    'alert-danger': quizResult.score_percentage < 50
                }">
                    Total Score: {{ quizResult.score_percentage.toFixed(2) }}%
                </div>
                <p>Correct Answers: {{ quizResult.correct_answers }} / {{ quizResult.total_questions }}</p>

                <!-- Detailed Results -->
                <div class="mt-4">
                    <h3 class="h5">Detailed Results</h3>
                    <div v-for="(result, index) in quizResult.detailed_results" :key="result.question_id"
                        class="mb-3 p-3 border rounded" :class="{
                            'bg-success bg-opacity-10': result.is_correct,
                            'bg-danger bg-opacity-10': !result.is_correct
                        }">
                        <p>Question {{ index + 1 }}: <span class="fw-bold" :class="{
                            'text-success': result.is_correct,
                            'text-danger': !result.is_correct
                        }">{{ result.is_correct ? 'Correct' : 'Incorrect' }}</span></p>
                        <p>Your Answer: Option {{ result.selected_option }}</p>
                        <p>Correct Answer: Option {{ result.correct_option }}</p>
                    </div>
                </div>
                <button @click="returnToDashboard" class="btn btn-primary mt-4">Return to Dashboard</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            quizId: null,
            questions: [],
            selectedAnswers: [],
            currentQuestionIndex: 0,
            loading: true,
            error: null,
            quizSubmitted: false,
            quizResult: null,
            timeRemaining: 0,
            timer: null
        }
    },
    computed: {
        currentQuestion() {
            return this.questions[this.currentQuestionIndex];
        },
        formattedTimeRemaining() {
            const minutes = Math.floor(this.timeRemaining / 60);
            const seconds = this.timeRemaining % 60;
            return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    },
    mounted() {
        this.quizId = this.$route.params.quizId;
        this.fetchQuizQuestions();
    },
    methods: {
        async fetchQuizQuestions() {
            try {
                this.loading = true;
                const studentToken = localStorage.getItem('student_token');

                const res = await fetch(`http://127.0.0.1:5000/student/quiz/${this.quizId}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${studentToken}`,
                        'Content-Type': 'application/json'
                    }
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.message || 'Failed to fetch quiz questions');
                }

                this.questions = data.questions;
                this.selectedAnswers = new Array(this.questions.length).fill(null);
                this.loading = false;
                this.startTimer(data.time_duration);
            } catch (error) {
                console.error('Error fetching quiz questions:', error.message);
                alert(error.message);
                this.$router.push('/student-dashboard');
            }
        },

        startTimer(time_duration) {
            this.timeRemaining = time_duration * 60;
            this.timer = setInterval(() => {
                this.timeRemaining--;
                if (this.timeRemaining <= 0) {
                    this.submitQuiz();
                }
            }, 1000);
        },
        nextQuestion() {
            this.currentQuestionIndex++;
        },
        previousQuestion() {
            this.currentQuestionIndex--;
        },
        logout() {
            // Implement logout logic
            localStorage.removeItem('student_token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        },
        submitQuiz() {
            clearInterval(this.timer);
            const studentToken = localStorage.getItem('student_token');
            const answers = this.selectedAnswers.map((answer, index) => ({
                question_id: this.questions[index].id,
                selected_option: answer
            }));

            fetch(`http://127.0.0.1:5000/student/quiz/${this.quizId}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${studentToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ answers })
            })
                .then(response => response.json())
                .then(result => {
                    this.quizResult = result;
                    this.quizSubmitted = true;
                })
                .catch(error => {
                    console.error('Error submitting quiz:', error);
                    this.error = 'Failed to submit quiz. Please try again.';
                });
        },
        returnToDashboard() {
            this.$router.push('/student-dashboard');
        }
    },
    beforeUnmount() {
        clearInterval(this.timer);
    }
}
</script>

<style scoped></style>