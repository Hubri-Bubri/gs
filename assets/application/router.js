import VueRouter from 'vue-router';
import LoginForm from '@/component/login-form/index';
import Dashboard from '@/component/dashboard/index';


const router = new VueRouter({
    routes: [
        {path: "/", component: Dashboard},
        {path: "/login", component: LoginForm}
    ]
});

export {router};
