import {createRouter, createWebHistory} from 'vue-router'
import LoginPage from "@/pages/LoginPage.vue";
import AccountPage from "@/pages/AccountPage.vue";
import ResearchPage from "@/pages/ResearchPage.vue";
import CreateResearch from "@/pages/CreatePage.vue";

const routes = [
  {path: '/', component: LoginPage},
  {path: '/account', component: AccountPage},
  {path: '/research/:id', component: ResearchPage},
  {path: '/create', component: CreateResearch}

]

const router = createRouter({
  history: createWebHistory(), routes
})

export default router
