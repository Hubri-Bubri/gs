import VueRouter from 'vue-router';
import HelloWorld from '@/component/hello-world/index';


const router = new VueRouter({
    routes: [
        {path: "/", component: HelloWorld}
    ]
});

export {router};
