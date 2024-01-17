import VueRouter from 'vue-router';
import ProjectMaster from '@business/component/project/master';
import ProjectDetail from '@business/component/project/detail';
import ProjectUser from '@business/component/project/user';
import CustomerMaster from '@business/component/customer/master';
import CustomerDetail from '@business/component/customer/detail';
import PricesMaster from '@business/component/prices/master';
import ReportsMaster from '@business/component/reports/master';
import DevicesMaster from '@business/component/devices/master';
import PersonalMaster from '@business/component/personals/master';
import BalanceMaster from '@business/component/balance/master';

import OffersMaster from '@business/component/offers/master';
import ContractsMaster from '@business/component/contracts/master';
import SubContractsMaster from '@business/component/subContracts/master';

import SubMaster from '@business/component/sub/master';
import SubDetail from '@business/component/sub/detail';


import Form from '@business/component/form/master';

import Error404 from '@share/component/special/error-404';


const router = new VueRouter({
    routes: [
        {path: "/", component: ProjectMaster},
        {path: "/project", component: ProjectMaster},
        {path: "/project/detail/:id", component: ProjectDetail, props: true},
        {path: "/I/:user/:id/:foolder", component: ProjectUser, props: true},
        {path: "/customer", component: CustomerMaster},
        {path: "/customer/detail/:id", component: CustomerDetail, props: true},
        {path: "/prices", component: PricesMaster},
        {path: "/reports", component: ReportsMaster},
        {path: "/devices", component: DevicesMaster},
        {path: "/personals", component: PersonalMaster},
        {path: "/balance", component: BalanceMaster},

        {path: "/offers", component: OffersMaster},
        {path: "/contracts", component: ContractsMaster},
        {path: "/subcontracts", component: SubContractsMaster},
        
        {path: "/form", component: Form},
        {path: "*", component: Error404},
        {path: "/sub", component: SubMaster},
        {path: "/sub/detail/:id", component: SubDetail, props: true}
    ]
});

export {router};
