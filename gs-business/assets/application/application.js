import Vue from 'vue';
// import BootstrapVue from 'bootstrap-vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import VueRouter from 'vue-router';
// import VueI18n from 'vue-i18n';

import VueI18n from 'vue-i18n';



// import VueSelect from 'vue-select';
// import LiquorTree from 'liquor-tree';
// import InfiniteScroll from 'v-infinite-scroll';
// import 'v-infinite-scroll/dist/v-infinite-scroll.css';
import Clipboard from 'v-clipboard';
// import VueColumnsResizable from 'vue-columns-resizable';

// import XrxVue from '@share/component/xrx-vue/App.vue';
// import GsPaint from '@share/component/xrx-vue/App.vue';
// import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
// Vue.use(IconsPlugin);


// import GsPaint from 'gs-paint/src/Editor.vue';
// import GsPaint from 'gs-paint/src/demo/Demo.vue';
import { GsEditorPlugin } from 'gs-paint/src/';


import Container from '@share/component/container/container';
import Security from '@security/plugin/security/index';
import ContainerHeader from '@share/component/container/container-header';
import ContainerBody from '@share/component/container/container-body';
import ContainerFooter from '@share/component/container/container-footer';
import TopMenu from '@business/component/top-menu/index';

import CalcTableGroup from '@share/component/calc-table/calc-table-group';
import CalcTableGroupPrint from '@share/component/calc-table/calc-table-group-print';
import CalcTable from '@share/component/calc-table/calc-table';
import CalcTablePrint from '@share/component/calc-table/calc-table-print';
import calculation from '@share/component/calc-table/calculation';
import calculationPrint from '@share/component/calc-table/calculation-print';
import print from '@share/component/print/print';
import project from '@share/component/project/project';
import docs from '@share/component/project/docs';
import images from '@share/component/project/images';

import DamagesTableGroup from '@share/component/damages/damages-table-group';
import DamagesTable from '@share/component/damages/damages-table';
import damage from '@share/component/project/damage';

import DevicesTableGroup from '@share/component/devices/devices-table-group';
import DevicesTable from '@share/component/devices/devices-table';
import DevicesMeasurement from '@share/component/devices/devices-measurement';

import edit from '@share/component/project/edit';
import edevices from '@share/component/project/edevices';

import price from '@share/component/price/price';
import devices from '@share/component/devices/devices';

// import balance from '@share/component/balance/balance';




// import CKEditor from '@ckeditor/ckeditor5-vue2';

import Spinner from 'vue-simple-spinner'
import LineChart from '@share/component/charts/LineChart.vue';
// import LineChart from '@share/component/charts/LineChart1.js';
import VueDragTree from '@share/component/tree';
// import 'vue-drag-tree/dist/vue-drag-tree.min.css'

import '@share/style/bootstrap.scss';
import '@share/style/override/card.scss';
import '@share/style/component/container.scss';
import '@share/style/component/top-menu.scss';
import '@share/style/layout.scss';
import '@share/style/component/special.scss';
import '@share/style/component/loader.scss';

import axios from 'axios';
import { router } from '@business/router';

import thousandSeparator from '@share/thousandSeparator';
import reThousandSeparator from '@share/reThousandSeparator';

import dateInverse from '@share/date';

import Viewer from 'v-viewer';
import 'viewerjs/dist/viewer.css';

import gb from './gb.json';
import de from './de.json';
import ru from './ru.json';

Vue.use(VueI18n);

const messages = {
    gb,
    de,
    ru
};

const i18n = new VueI18n({
  locale: window.navigator.language.slice(0, 2), 
  fallbackLocale: 'gb',
  messages, // set locale messages
});

new Vue({ i18n: i18n});
import VueNativeSock from 'vue-native-websocket'
// console.log(window.location.host)
//Vue.use(VueNativeSock, 'ws://'+window.location.host+'/ws', {
var protocolType = 'wss'
if (window.location.protocol=='http:') protocolType = 'ws'
Vue.use(VueNativeSock, protocolType+'://'+window.location.host+'/ws', { 

//Vue.use(VueNativeSock, 'ws://127.0.0.1:8081/ws', { 

// Vue.use(VueNativeSock, 'ws://it-vision.pro:8081/ws', { 
  reconnection: true, // (Boolean) whether to reconnect automatically (false)
  reconnectionAttempts: Infinity, // (Number) number of reconnection attempts before giving up (Infinity),
  reconnectionDelay: 10, // (Number) how long to initially wait before attempting a new (1000)
})
const vm = new Vue()
vm.$options.sockets.onerror = (data) => {
    // alert('Reconnecting...')
    // window.location.reload();
}
Vue.use(VueDragTree);
Vue.use(Viewer);
Vue.use(VueRouter);
Vue.use(BootstrapVue);
Vue.use(Security);
// Vue.use(InfiniteScroll);
Vue.use(Clipboard);
Vue.use(IconsPlugin);
// Vue.use( CKEditor );
Vue.use(GsEditorPlugin);

// Vue.component('gs-paint', GsPaint);
// Vue.component('VSelect', VueSelect);
Vue.component('Container', Container);
Vue.component('ContainerHeader', ContainerHeader);
Vue.component('ContainerBody', ContainerBody);
Vue.component('ContainerFooter', ContainerFooter);
// Vue.component(LiquorTree.name, LiquorTree);
Vue.component('TopMenu', TopMenu);

Vue.component('calc-table-group', CalcTableGroup);
Vue.component('calc-table', CalcTable);
Vue.component('calc-table-group-print', CalcTableGroupPrint);
Vue.component('calc-table-print', CalcTablePrint);
Vue.component('calculation', calculation);
Vue.component('calculation-print', calculationPrint);
Vue.component('project', project);
Vue.component('docs', docs);
Vue.component('images', images);
Vue.component('edit', edit);
Vue.component('edevices', edevices);

Vue.component('damage', damage);

Vue.component('damages-table-group', DamagesTableGroup);
Vue.component('damages-table', DamagesTable);

Vue.component('devices-table-group', DevicesTableGroup);
Vue.component('devices-table', DevicesTable);
Vue.component('devices-measurement', DevicesMeasurement);

Vue.component('price', price);
Vue.component('devices', devices);

Vue.component('print', print);
// Vue.component('balance', balance);
Vue.component('LineChart', LineChart);

Vue.component('Spinner', Spinner);


// Vue.use(VueColumnsResizable);



 axios.get('/profile', {
        params: {
          'subDomain': window.location.href.split('//')[1].split('.awe.do')[0]
        }
      }).then(response => {
    if(window.location.href.indexOf('/I/')==-1){ 
        if(response.data.account == null) {
            window.location.href = '//in.awe.do';
        }
    } 
    // console.log(response.data)
    return new Vue({
        i18n,
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
                    'available-companies': {},
                    'selected-company': {},
                    'access': [],
                    'roles': []
                }
            }
        }
    });

});

Vue.filter('thousandSeparator', thousandSeparator);
Vue.filter('reThousandSeparator', reThousandSeparator);
Vue.filter('dateInverse', dateInverse);

// window.mouseover = () =>{
//     window.onbeforeunload = null;
// };
// window.onmouseout = () =>{
//     window.onbeforeunload = null;
// };
// function exit() {
//     axios.get('/logout').then(response => console.log('exit'));
// };
// var prevKey="";
// document.onkeydown =(function (e) {            
//     if (e.key=="F5") {
//         window.onbeforeunload = null;
//     }
//     else if (e.key.toUpperCase() == "W" && prevKey == "CONTROL") {                
//         window.onbeforeunload = exit;   
//     }
//     else if (e.key.toUpperCase() == "R" && prevKey == "CONTROL") {
//         window.onbeforeunload = null;
//     }
//     else if (e.key.toUpperCase() == "F4" && (prevKey == "ALT" || prevKey == "CONTROL")) {
//         window.onbeforeunload = exit;
//     }
//     prevKey = e.key.toUpperCase();
// });