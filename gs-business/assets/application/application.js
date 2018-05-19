import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';
import vSelect from 'vue-select';

import Container from '@share/component/container/container';
import ContainerHeader from '@share/component/container/container-header';
import ContainerBody from '@share/component/container/container-body';
import ContainerFooter from '@share/component/container/container-footer';

import TopMenu from '@business/component/top-menu/index';


import '@share/style/override/card.scss';
import '@share/style/component/container.scss';
import '@share/style/component/top-menu.scss';
import '@share/style/layout.scss';
import '@share/style/component/special.scss';


import {router} from '@business/router';


Vue.use(VueRouter);
Vue.use(BootstrapVue);

Vue.component('v-select', vSelect);
Vue.component('Container', Container);
Vue.component('ContainerHeader', ContainerHeader);
Vue.component('ContainerBody', ContainerBody);
Vue.component('ContainerFooter', ContainerFooter);

Vue.component('TopMenu', TopMenu);

const application = new Vue({
    router,
    el: ".gs-business"
});

