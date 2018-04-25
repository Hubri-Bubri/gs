import VueRouter from 'vue-router';
import Login from '@/component/login/index';


const router = new VueRouter({
    routes: [
        {path: "/", component: Login},
        {path: "/login", component: Login}
    ]
});

export {router};
