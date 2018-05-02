import VueRouter from 'vue-router';
import HelloWorld from '@/component/hello-world/index';
import Info from '@/component/info/index';


const router = new VueRouter({
    routes: [
        {path: "/", component: HelloWorld},
        {path: "/info", component: Info}
    ]
});

export {router};
