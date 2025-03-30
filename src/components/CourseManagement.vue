<template>
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5>Course Management</h5>
            <button class="btn btn-primary btn-sm" @click="openCourseModal('add')">
                Add Course
            </button>
        </div>
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th style="width: 15px">ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th style="width: 130px">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="course in courses" :key="course.id">
                        <td>{{ course.id }}</td>
                        <td>{{ course.name }}</td>
                        <td>{{ course.description }}</td>
                        <td>
                            <button class="btn btn-sm btn-warning me-2" @click="openCourseModal('edit', course)">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger" @click="deleteCourse(course.id)">
                                Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Course Modal -->
        <div class="modal fade" id="courseModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ modalTitle }} Course</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitCourse">
                            <div class="mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" class="form-control" v-model="courseForm.name" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Description</label>
                                <textarea class="form-control" v-model="courseForm.description" required></textarea>
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
    name: 'CourseManagement',
    data() {
        return {
            courses: [],
            courseForm: {
                name: '',
                description: ''
            },
            modalTitle: 'Add',
            editMode: false,
            editCourseId: null
        }
    },
    mounted() {
        this.fetchCourses()
    },
    methods: {
        async fetchCourses() {
            try {
                const token = localStorage.getItem('admin_token')
                const response = await fetch('http://127.0.0.1:5000/admin/courses', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })

                if (!response.ok) {
                    throw new Error('Failed to fetch courses')
                }

                this.courses = await response.json()
            } catch (error) {
                console.error('Error fetching courses:', error)
                // Optionally show error message to user
            }
        },
        async submitCourse() {
            try {
                const token = localStorage.getItem('admin_token')
                const url = this.editMode
                    ? `http://127.0.0.1:5000/admin/courses/${this.editCourseId}`
                    : 'http://127.0.0.1:5000/admin/courses'

                const method = this.editMode ? 'PUT' : 'POST'

                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.courseForm)
                })

                if (!response.ok) {
                    throw new Error('Failed to save course')
                }

                await this.fetchCourses()
                // Use vanilla JavaScript to hide the modal when using CDN
                const modalElement = document.getElementById('courseModal')
                const modalInstance = bootstrap.Modal.getInstance(modalElement)
                if (modalInstance) {
                    modalInstance.hide()
                } else {
                    new bootstrap.Modal(modalElement).hide()
                }
            } catch (error) {
                console.error('Error saving course:', error)
                // Optionally show error message to user
            }
        },
        async deleteCourse(courseId) {
            if (confirm('Are you sure you want to delete this course?')) {
                try {
                    const token = localStorage.getItem('admin_token')
                    const response = await fetch(`http://127.0.0.1:5000/admin/courses/${courseId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    })

                    if (!response.ok) {
                        throw new Error('Failed to delete course')
                    }

                    await this.fetchCourses()
                } catch (error) {
                    console.error('Error deleting course:', error)
                    // Optionally show error message to user
                }
            }
        },
        openCourseModal(mode, course = null) {
            this.editMode = mode === 'edit'
            this.modalTitle = this.editMode ? 'Edit' : 'Add'

            if (this.editMode && course) {
                this.courseForm.name = course.name
                this.courseForm.description = course.description
                this.editCourseId = course.id
            } else {
                this.courseForm.name = ''
                this.courseForm.description = ''
                this.editCourseId = null
            }

            // Use vanilla JavaScript to show the modal when using CDN
            const modalElement = document.getElementById('courseModal')
            const modalInstance = bootstrap.Modal.getInstance(modalElement)
            if (modalInstance) {
                modalInstance.show()
            } else {
                new bootstrap.Modal(modalElement).show()
            }
        },
    }
}
</script>