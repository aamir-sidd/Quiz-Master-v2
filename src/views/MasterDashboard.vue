<template>
  <div class="bg-light">
    <Navbar />
    <div class="container-fluid" style="overflow: auto; max-height: 95vh">
      <div class="row mt-4">
        <div class="col-12">
          <CourseManagement />
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-12">
          <ChapterManagement />
        </div>
      </div>
      <div class="row mt-4 mb-4">
        <div class="col-12">
          <QuizManagement />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'
import CourseManagement from '../components/CourseManagement.vue'
import ChapterManagement from '../components/ChapterManagement.vue'
import QuizManagement from '../components/QuizManagement.vue'

export default {
  name: 'AdminDashboard',
  components: {
    Navbar,
    CourseManagement,
    ChapterManagement,
    QuizManagement
  }
}
</script>