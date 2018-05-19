import {hasPermissionDirective, hasPermission} from '@security/directive/has-permission';


export default class Security {

    constructor(table) {

        table['access-user'] = _.each(table['access-user'], accessRule => {
            accessRule.permission = _.chain(accessRule.permission)
                .split(',')
                .map(premission => _.toNumber(premission))
                .value();
        });

        this.table = table;
        this.account = this.table['account'];
        this.company = this.table['selected-company'];
    }

    static install(Vue, options) {
        Vue.directive('has-permission', hasPermissionDirective);

        Vue.mixin({
            beforeCreate() {
                if (this.$options.security) {
                    this._security = this.$options.security;
                }
            }
        });

        Object.defineProperty(Vue.prototype, '$security', {
            get() {
                let component = this;

                while (true) {
                    if (component._security) {
                        return component._security;
                    } else if (component.$parent) {
                        component = component.$parent;
                    } else {
                        return;
                    }
                }
            }
        })
    }

    hasPermission(target, predicate) {
        return hasPermission(this.table['access-user'], target, predicate);
    }
}
