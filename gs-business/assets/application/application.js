import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';
import vSelect from 'vue-select';

import Container from '@share/component/container/container';
import Security from '@security/plugin/security/index';
import ContainerHeader from '@share/component/container/container-header';
import ContainerBody from '@share/component/container/container-body';
import ContainerFooter from '@share/component/container/container-footer';

import TopMenu from '@business/component/top-menu/index';

import '@share/style/override/card.scss';
import '@share/style/component/container.scss';
import '@share/style/component/top-menu.scss';
import '@share/style/layout.scss';
import '@share/style/component/special.scss';
import '@share/style/component/loader.scss';

import axios from 'axios';
import { router } from '@business/router';

Vue.use(VueRouter);
Vue.use(BootstrapVue);
Vue.use(Security);

Vue.component('v-select', vSelect);
Vue.component('Container', Container);
Vue.component('ContainerHeader', ContainerHeader);
Vue.component('ContainerBody', ContainerBody);
Vue.component('ContainerFooter', ContainerFooter);

Vue.component('TopMenu', TopMenu);


axios.get('/profile').then(response => {
    return new Vue({
        security: new Security(response.data),
        // security: new Security({
            // account ...
        // }),
        router: router,
        el: "#application",
        data() {
            return {
                profile: {
                    'account': {},
                    'selected-company': {},
                    'access': [],
                    'roles': []
                }
            }
        }
    });
});
