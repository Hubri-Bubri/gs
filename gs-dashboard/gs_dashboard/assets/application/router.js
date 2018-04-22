import VueRouter from 'vue-router';
import LoginForm from '@/component/login-form/index';
import Dashboard from '@/component/dashboard/index';
import BaerGS from '@/component/BaerGS/index';
import tempNav from '@/component/tempNav/index';


const router = new VueRouter({
    routes: [
        {path: "/", component: Dashboard},
        {path: "/login", component: LoginForm},
        {path: "/BaerGS", component: BaerGS}
    ]
});

export {router};
