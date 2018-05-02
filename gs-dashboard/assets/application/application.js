import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import {router} from '@dashboard/router';
import Layout from '@dashboard/component/layout/index';

import Login from '@dashboard/component/login/index';


import '@dashboard/style/css/layout.css'
import '@dashboard/style/css/login.css'

// include vue.js plugins
Vue.use(VueRouter);
Vue.use(BootstrapVue);


// include own vue.js components
Vue.component('Layout', Layout);
Vue.component('Login', Login);

const application = new Vue({
    router,
    el: ".gs-dashboard"
});

