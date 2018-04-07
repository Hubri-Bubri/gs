import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';

import {router} from '@/router';

import LoginForm from '@/component/login-form/index';
import Dashboard from '@/component/dashboard/index';
import Layout from '@/component/layout/index';

// include vue.js plugins
Vue.use(VueRouter);
Vue.use(BootstrapVue);

// include own vue.js components
Vue.component('Layout', Layout);
Vue.component('LoginForm', LoginForm);


const application = new Vue({router, el: ".application"});
