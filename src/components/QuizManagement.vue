<template>
  <div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5>Quiz Management</h5>
      <button class="btn btn-primary btn-sm" @click="openQuizModal('add')">
        Add Quiz
      </button>
    </div>
    <div class="card-body">
      <table class="table table-striped">
        <thead>
          <tr>
            <th style="width: 15px">ID</th>
            <th>Chapter</th>
            <th>Date</th>
            <th>Duration</th>
            <th>Remarks</th>
            <th style="width: 230px">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="quiz in quizzes" :key="quiz.id">
            <td>{{ quiz.id }}</td>
            <td>{{ quiz.chapter_name }}</td>
            <td>{{ quiz.date_of_quiz }}</td>
            <td>{{ quiz.time_duration }} minutes</td>
            <td>{{ quiz.remarks || 'N/A' }}</td>
            <td>
              <div class="btn-group">
                <button class="btn btn-sm btn-info" @click="viewQuizQuestions(quiz.id)">
                  View Questions
                </button>
                <button class="btn btn-sm btn-warning" @click="openQuizModal('edit', quiz)">
                  Edit
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteQuiz(quiz.id)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Quiz Modal -->
    <div class="modal fade" id="quizModal" tabindex="-1" ref="quizModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalTitle }} Quiz</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitQuiz">
              <div class="mb-3">
                <label class="form-label">Chapter</label>
                <select class="form-select" v-model="quizForm.chapter_id" required>
                  <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                    {{ chapter.name }}
                  </option>
                </select>
              </div>
            
              <div class="mb-3">
                <label class="form-label">Date of Quiz</label>
                <input type="date" class="form-control" v-model="quizForm.date_of_quiz" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Time Duration (minutes)</label>
                <input type="number" class="form-control" v-model="quizForm.time_duration" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Remarks</label>
                <textarea class="form-control" v-model="quizForm.remarks"></textarea>
              </div>
              <button type="submit" class="btn btn-primary">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Quiz Questions Modal -->
    <div class="modal fade" id="questionsModal" tabindex="-1" ref="questionsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Quiz Questions</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <button class="btn btn-primary mb-3" @click="openQuestionModal('add')">
              Add Question
            </button>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Question</th>
                  <th>Options</th>
                  <th>Correct Option</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="question in questions" :key="question.id">
                  <td>{{ question.question_statement }}</td>
                  <td>
                    1. {{ question.option1 }}<br>
                    2. {{ question.option2 }}<br>
                    3. {{ question.option3 }}<br>
                    4. {{ question.option4 }}
                  </td>
                  <td>{{ question.correct_option }}</td>
                  <td>
                    <button class="btn btn-sm btn-warning me-2" @click="openQuestionModal('edit', question)">
                      Edit
                    </button>
                    <button class="btn btn-sm btn-danger" @click="deleteQuestion(question.id)">
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Question Modal -->
    <div class="modal fade" id="questionModal" tabindex="-1" ref="questionModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ questionModalTitle }} Question</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitQuestion">
              <div class="mb-3">
                <label class="form-label">Question Statement</label>
                <textarea class="form-control" v-model="questionForm.question_statement" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 1</label>
                <input type="text" class="form-control" v-model="questionForm.option1" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 2</label>
                <input type="text" class="form-control" v-model="questionForm.option2" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 3</label>
                <input type="text" class="form-control" v-model="questionForm.option3" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 4</label>
                <input type="text" class="form-control" v-model="questionForm.option4" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Correct Option</label>
                <select class="form-select" v-model="questionForm.correct_option" required>
                  <option value="1">Option 1</option>
                  <option value="2">Option 2</option>
                  <option value="3">Option 3</option>
                  <option value="4">Option 4</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuizManagement',
  data() {
    return {
      quizzes: [],
      chapters: [],
      quizForm: {
        chapter_id: null,
        date_of_quiz: '',
        time_duration: null,
        remarks: ''
      },
      modalTitle: 'Add',
      editMode: false,
      editQuizId: null,

      questions: [],
      currentQuizId: null,
      questionForm: {
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      },
      questionModalTitle: 'Add',
      editQuestionMode: false,
      editQuestionId: null
    }
  },
  mounted() {
    this.fetchChapters()
    this.fetchQuizzes()
  },
  methods: {
    openQuizModal(mode, quiz = null) {
      this.editMode = mode === 'edit'
      this.modalTitle = this.editMode ? 'Edit' : 'Add'

      if (this.editMode && quiz) {
        this.editQuizId = quiz.id
        this.quizForm = { ...quiz }
      } else {
        this.quizForm = {
          chapter_id: null,
          date_of_quiz: '',
          time_duration: null,
          remarks: ''
        }
      }

      const modal = new bootstrap.Modal(this.$refs.quizModal)
      modal.show()
    },
    openQuestionModal(mode, question = null) {
      this.editQuestionMode = mode === 'edit'
      this.questionModalTitle = this.editQuestionMode ? 'Edit' : 'Add'

      if (this.editQuestionMode && question) {
        this.editQuestionId = question.id
        this.questionForm = { ...question }
      } else {
        this.questionForm = {
          question_statement: '',
          option1: '',
          option2: '',
          option3: '',
          option4: '',
          correct_option: ''
        }
      }

      const modal = new bootstrap.Modal(this.$refs.questionModal)
      modal.show()
    },
    async fetchChapters() {
      try {
        const token = localStorage.getItem('admin_token')
        const response = await fetch('http://127.0.0.1:5000/admin/chapters', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to fetch chapters')
        }

        this.chapters = await response.json()
      } catch (error) {
        console.error('Error fetching chapters:', error)
      }
    },
    async fetchQuizzes() {
      try {
        const token = localStorage.getItem('admin_token')
        const response = await fetch('http://127.0.0.1:5000/admin/quizzes', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to fetch quizzes')
        }

        this.quizzes = await response.json()
      } catch (error) {
        console.error('Error fetching quizzes:', error)
      }
    },
    async submitQuiz() {
      try {
        const token = localStorage.getItem('admin_token')
        const url = this.editMode
          ? `http://127.0.0.1:5000/admin/quiz/${this.editQuizId}`
          : `http://127.0.0.1:5000/admin/quiz/${this.quizForm.chapter_id}`

        const method = this.editMode ? 'PUT' : 'POST'

        const response = await fetch(url, {
          method: method,
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.quizForm)
        })

        if (!response.ok) {
          throw new Error('Failed to save quiz')
        }

        await this.fetchQuizzes()
        const modal = bootstrap.Modal.getInstance(this.$refs.quizModal)
        modal.hide()
      } catch (error) {
        console.error('Error saving quiz:', error)
      }
    },
    async deleteQuiz(quizId) {
      if (confirm('Are you sure you want to delete this quiz?')) {
        try {
          const token = localStorage.getItem('admin_token')
          const response = await fetch(`http://127.0.0.1:5000/admin/quiz/${quizId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })

          if (!response.ok) {
            throw new Error('Failed to delete quiz')
          }

          await this.fetchQuizzes()
        } catch (error) {
          console.error('Error deleting quiz:', error)
        }
      }
    },
    async viewQuizQuestions(quizId) {
      try {
        const token = localStorage.getItem('admin_token')
        const response = await fetch(`http://127.0.0.1:5000/admin/questions/${quizId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to fetch quiz questions')
        }

        this.currentQuizId = quizId
        this.questions = await response.json()
        const modal = new bootstrap.Modal(this.$refs.questionsModal)
        modal.show()
      } catch (error) {
        console.error('Error fetching quiz questions:', error)
      }
    },
    async submitQuestion() {
      try {
        const token = localStorage.getItem('admin_token')
        const url = this.editQuestionMode
          ? `http://127.0.0.1:5000/admin/question/${this.editQuestionId}`
          : `http://127.0.0.1:5000/admin/question/${this.currentQuizId}`

        const method = this.editQuestionMode ? 'PUT' : 'POST'

        const response = await fetch(url, {
          method: method,
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.questionForm)
        })

        if (!response.ok) {
          throw new Error('Failed to save question')
        }

        await this.viewQuizQuestions(this.currentQuizId)
        const modal = bootstrap.Modal.getInstance(this.$refs.questionModal)
        modal.hide()
      } catch (error) {
        console.error('Error saving question:', error)
      }
    },
    async deleteQuestion(questionId) {
      if (confirm('Are you sure you want to delete this question?')) {
        try {
          const token = localStorage.getItem('admin_token')
          const response = await fetch(`http://127.0.0.1:5000/admin/question/${questionId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })

          if (!response.ok) {
            throw new Error('Failed to delete question')
          }

          await this.viewQuizQuestions(this.currentQuizId)
        } catch (error) {
          console.error('Error deleting question:', error)
        }
      }
    }
  }
}
</script>