import { createRouter, createWebHashHistory } from "vue-router";
import LandingView from "@/views/Home.vue"

const routes = [
  {
    path: "/",
    name: "landing",
    component: LandingView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
