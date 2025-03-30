<template>
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5>Chapter Management</h5>
            <button class="btn btn-primary btn-sm" @click="openChapterModal('add')">
                Add Chapter
            </button>
        </div>
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th style="width: 15px">ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Course</th>
                        <th style="width: 130px">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="chapter in chapters" :key="chapter.id">
                        <td>{{ chapter.id }}</td>
                        <td>{{ chapter.name }}</td>
                        <td>{{ chapter.description }}</td>
                        <td>{{ chapter.course_name }}</td>
                        <td>
                            <button class="btn btn-sm btn-warning me-2" @click="openChapterModal('edit', chapter)">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger" @click="deleteChapter(chapter.id)">
                                Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Chapter Modal -->
        <div class="modal fade" id="chapterModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ modalTitle }} Chapter</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitChapter">
                            <div class="mb-3">
                                <label class="form-label">Course</label>
                                <select class="form-select" v-model="chapterForm.course_id" required>
                                    <option v-for="course in courses" :key="course.id" :value="course.id">
                                        {{ course.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" class="form-control" v-model="chapterForm.name" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Description</label>
                                <textarea class="form-control" v-model="chapterForm.description" required></textarea>
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
    name: 'ChapterManagement',
    data() {
        return {
            chapters: [],
            courses: [],
            chapterForm: {
                course_id: null,
                name: '',
                description: ''
            },
            modalTitle: 'Add',
            editMode: false,
            editChapterId: null
        }
    },
    mounted() {
        this.fetchCourses()
        this.fetchChapters()
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
        async submitChapter() {
            try {
                const token = localStorage.getItem('admin_token')
                const url = this.editMode
                    ? `http://127.0.0.1:5000/admin/chapter/${this.editChapterId}`
                    : `http://127.0.0.1:5000/admin/chapter/${this.chapterForm.course_id}`

                const method = this.editMode ? 'PUT' : 'POST'

                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.chapterForm)
                })

                if (!response.ok) {
                    throw new Error('Failed to save chapter')
                }

                await this.fetchChapters()
                // Use vanilla JavaScript to hide the modal when using CDN
                const modalElement = document.getElementById('chapterModal')
                const modalInstance = bootstrap.Modal.getInstance(modalElement)
                if (modalInstance) {
                    modalInstance.hide()
                } else {
                    new bootstrap.Modal(modalElement).hide()
                }
            } catch (error) {
                console.error('Error saving chapter:', error)
            }
        },
        async deleteChapter(chapterId) {
            if (confirm('Are you sure you want to delete this chapter?')) {
                try {
                    const token = localStorage.getItem('admin_token')
                    const response = await fetch(`http://127.0.0.1:5000/admin/chapter/${chapterId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    })

                    if (!response.ok) {
                        throw new Error('Failed to delete chapter')
                    }

                    await this.fetchChapters()
                } catch (error) {
                    console.error('Error deleting chapter:', error)
                }
            }
        },
        openChapterModal(mode, chapter = null) {
            this.editMode = mode === 'edit'
            this.modalTitle = this.editMode ? 'Edit' : 'Add'

            if (this.editMode && chapter) {
                this.chapterForm.course_id = chapter.course_id
                this.chapterForm.name = chapter.name
                this.chapterForm.description = chapter.description
                this.editChapterId = chapter.id
            } else {
                this.chapterForm.course_id = null
                this.chapterForm.name = ''
                this.chapterForm.description = ''
                this.editChapterId = null
            }

            // Use vanilla JavaScript to show the modal when using CDN
            const modalElement = document.getElementById('chapterModal')
            const modalInstance = bootstrap.Modal.getInstance(modalElement)
            if (modalInstance) {
                modalInstance.show()
            } else {
                new bootstrap.Modal(modalElement).show()
            }
        }
    }
}
</script>