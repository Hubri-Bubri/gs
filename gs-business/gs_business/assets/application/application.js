import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import {router} from '@/router';
import Layout from '@/component/layout/index';

import '@/style/css/layout.css'
import '@/style/css/login.css'

// include vue.js plugins
Vue.use(VueRouter);
Vue.use(BootstrapVue);


// include own vue.js components
Vue.component('Layout', Layout);

const application = new Vue({
    router,
    el: ".gs-business"
});

