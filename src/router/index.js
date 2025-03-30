import {createRouter, createWebHistory} from "vue-router";
import RegisterUser from "../views/RegisterUser.vue";
import MasterDashboard from "../views/MasterDashboard.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import TakeQuiz from "../views/TakeQuiz.vue";
import LoginUser from "../views/LoginUser.vue";


const routes = [
    {path: "/", component: LoginUser},
    {path: "/login", component: LoginUser},
    {path: "/register", component: RegisterUser},
    {path: "/master-dashboard", component: MasterDashboard},
    {path: "/student-dashboard", component: StudentDashboard},
    {path: "/student/take-quiz/:quizId", component: TakeQuiz},
]


const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;