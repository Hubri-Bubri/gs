<template>
    <div class="gs-business-top-menu gs-top-menu">
        <div class="row no-gutters">
            <div class="col-8">
                <b-nav>
                    <b-nav-item-dropdown text="Project">
                        <b-dropdown-item to="/project" href="#">Projects</b-dropdown-item>
                        <b-dropdown-item to="/deals" href="#">Deals</b-dropdown-item>
                        <b-dropdown-item href="#">Assignments</b-dropdown-item>
                        <b-dropdown-item href="#">Bills</b-dropdown-item>
                        <b-dropdown-item href="#">OP-Balancing</b-dropdown-item>
                    </b-nav-item-dropdown>

                    <b-nav-item-dropdown text="Order Overview">
                        <b-dropdown-item href="#">T-Course</b-dropdown-item>
                        <b-dropdown-item href="#">Damage Reports</b-dropdown-item>
                        <b-dropdown-item href="#">Leakage Reports</b-dropdown-item>
                        <b-dropdown-item href="#">Device List</b-dropdown-item>
                        <b-dropdown-item href="#">Equipment Storage</b-dropdown-item>
                    </b-nav-item-dropdown>

                    <b-nav-item-dropdown text="SUB-Entrepreneur">
                        <b-dropdown-item href="#">SUB-Data</b-dropdown-item>
                        <b-dropdown-item href="#">SUB-Orders</b-dropdown-item>
                        <b-dropdown-item href="#">E-Invoices</b-dropdown-item>
                    </b-nav-item-dropdown>
                    
                    <b-nav-item-dropdown text="Base Data">
                        <b-dropdown-item href="#">Customer Data</b-dropdown-item>
                        <b-dropdown-item href="#">Contact Person</b-dropdown-item>
                        <b-dropdown-item href="#">Insurance</b-dropdown-item>
                        <b-dropdown-item href="#">Expert</b-dropdown-item>
                    </b-nav-item-dropdown>

                    <b-nav-item-dropdown text="Statistics">
                        <b-dropdown-item href="#">Monthly Sales</b-dropdown-item>
                        <b-dropdown-item href="#">Customer Sales</b-dropdown-item>
                        <b-dropdown-item href="#">Partner Sales</b-dropdown-item>
                    </b-nav-item-dropdown>

                    <b-nav-item-dropdown text="Settings" right v-has-permission.project@master@table-project.read>
                        <b-dropdown-item href="#">Employee</b-dropdown-item>
                        <b-dropdown-item href="#">Settings</b-dropdown-item>
                        <b-dropdown-item href="#">Units</b-dropdown-item>
                        <b-dropdown-item href="#" v-has-permission.project@master@table-project.write>Fleet</b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-nav>
            </div>

            <div class="col-4">
                <b-nav class="justify-content-end">
                    <b-nav-item-dropdown right>
                        <template slot="button-content">
                            <i class="fas fa-user"></i> {{username}} ({{company}})
                        </template>
                        <b-dropdown-item href="#">Profile</b-dropdown-item>
                        <b-dropdown-item href="#">Exit</b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-nav>
            </div>
        </div>
    </div>
</template>


<script type="text/javascript">
export default {
    computed: {

        username() {
            return `${this.$security.account['first_name']} ${this.$security.account['second_name']}`;
        },

        company() {
            return this.$security.company['name'];
        }
    },

    created() {
        console.log(this.$security.hasPermission('project@master@table-project', 'write'));
    }
}
</script>
