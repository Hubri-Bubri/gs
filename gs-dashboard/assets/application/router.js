import VueRouter from 'vue-router';
import Login from '@dashboard/component/login/index';


const router = new VueRouter({
    routes: [
        {path: "/", component: Login},
        {path: "/login", component: Login}
    ]
});

export {router};
