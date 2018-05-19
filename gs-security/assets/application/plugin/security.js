import hasPermission from '@security/directive/has-permission';


export default class Security {

    constructor(table) {
        this.table = table;
        this.account = this.table['account'];
        this.company = this.table['selected-company'];
    }

    static install(Vue, options) {
        Vue.directive('has-permission', hasPermission);

        Vue.mixin({
            beforeCreate() {
                if (this.$options.security) {
                    this._security = this.$options.security;
                }
            }
        });

        Object.defineProperty(Vue.prototype, '$security', {
            get() {
                let self = this;

                while (true) {
                    if (self._security) {
                        return self._security;
                    } else if (self.$parent) {
                        self = self.$parent;
                    } else {
                        return;
                    }
                }
            }
        })
    }
}
