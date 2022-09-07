<template>
    <div class="gs-dashboard">
        <div class="gs-dashboard__login">

            <b-form @submit.stop.prevent="onSubmit">

                <b-alert :dismissible="true"
                         :show="success === false"
                         size="lg"
                         variant="danger"
                         @dismissed="success = null"><i class="far fa-frown"></i> Incorrect login or/and password</b-alert>

                <b-form-group id="gs-dashboard__field-login">
                    <b-form-input :disabled="success === true" id="login" size="lg" type="text" placeholder="Enter login" v-model="login"></b-form-input>
                </b-form-group>

                <b-form-group id="gs-dashboard__field-password">
                    <b-form-input :disabled="success === true" id="password" size="lg" type="password" placeholder="Enter password" v-model="password"></b-form-input>
                </b-form-group>

                <b-form-select :options="companyOptions" 
                               v-model="companyId"
                               v-if="success === true"
                               class="mb-3" size="lg"></b-form-select>

                <b-form-select :options="applicationsOptions"
                               v-model="applicationUri"
                               v-if="applications.length > 0"
                               class="mb-3" size="lg"></b-form-select>

                <div class="gs-dashboard__login-footer">
                    <b-button :disabled="applicationUri === null"
                              @click.prevent.stop="openApplication(companyId, applicationUri)"
                              v-if="applications.length > 0"
                              type="submit" size="lg"
                              class="float-right"
                              variant="primary">
                        <i class="fas fa-check-circle"></i>
                    </b-button>

                    <b-button v-if="companies.length === 0"
                              type="submit"
                              size="lg"
                              class="float-right"
                              variant="primary">
                        <i class="fas fa-sign-in-alt"></i>
                    </b-button>

                </div>

            </b-form>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data () {
            return {
                login: null,
                password: null,
                success: null,
                companyId: null,
                applicationUri: null,
                applications: [],
                companies: []
            }
        },

        computed: {
            applicationsOptions() {
                return this.applications.concat([{
                    text: "Please select application",
                    value: null
                }])
            },

            companyOptions() {
                return this.companies.concat([{
                    text: "Please select company",
                    value: null
                }])
            }
        },

        watch: {
            companyId(value) {
                if (value === null) {
                    this.applications = []
                } else {
                    axios.post('/session', {"company-id": value}).then(response => {
                        this.loadApplications(value);
                    });
                }
            }
        },

        methods: {
            onSubmit() {

                axios.post('/authenticate', {
                    login: this.login,
                    password: this.password
                }).then(response => {
                    this.success = true;
                    this.loadCompanies();
                }).catch(error => {
                    this.success = false;
                });
            },

            openApplication(companyId, applicationUri) {
                window.open(this.applicationUri, "_self");
            },

            loadCompanies() {
                axios.get('/company').then(response => {
                    this.companies = response.data.map(_ => ({
                        text: _.name,
                        value: _.id
                    }))
                });
            },

            loadApplications(companyId) {
                return axios.get('/application', {
                    params: {
                        "company-id": companyId
                    }
                }).then(response => {
                    return this.applications = response.data.map(_ => ({
                        text: `${_.name} (${_.link})`,
                        value: _.link
                    }))
                });
            }
        }
    }
</script>
