import VueRouter from 'vue-router';
import ProjectMaster from '@business/component/project/master';
import ProjectDetail from '@business/component/project/detail';
import Error404 from '@share/component/special/error-404';


const router = new VueRouter({
    routes: [
        {path: "/", component: ProjectMaster},
        {path: "/project", component: ProjectMaster},
        {path: "/project/detail/:id", component: ProjectDetail, props: true},
        {path: "*", component: Error404}
    ]
});

export {router};
