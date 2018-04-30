import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import Container from '@share/component/container/container';

import {router} from '@/router';

// include vue.js plugins
Vue.use(VueRouter);
Vue.use(BootstrapVue);


// include own vue.js components

const application = new Vue({
    router,
    el: ".gs-business"
});

