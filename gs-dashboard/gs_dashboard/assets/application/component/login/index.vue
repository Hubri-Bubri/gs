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

                <b-form-select :options="applications_options" v-model="link" v-if="success === true" class="mb-3" size="lg">
                </b-form-select>

                <div class="gs-dashboard__login-footer">
                    
                    <b-button :disabled="link == null"
                              @click="openApplication(link)"
                              v-if="applications.length > 0"
                              type="submit" size="lg"
                              class="float-right"
                              variant="primary">
                        <i class="fas fa-check-circle"></i>
                    </b-button>

                    <b-button v-else type="submit" size="lg" class="float-right" variant="primary">
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
                link: null,
                applications: []
            }
        },

        computed: {
            applications_options() {
                return this.applications.concat([{
                    text: "Please select appliction",
                    value: null
                }])
            }
        },

        methods: {
            onSubmit() {
                this.failure = false;

                axios.post('/authenticate', {
                    login: this.login,
                    password: this.password
                }).then(response => {
                    this.success = true;
                    this.loadApplications();
                }).catch(error => {
                    this.success = false;
                });
            },

            openApplication(link) {
                window.open(link, '_blank');
            },

            loadApplications() {

                axios.get('/application').then(response => {
                    this.applications = response.data.map(_ => ({
                        text: _.name,
                        value: _.link
                    }))
                });
            }
        }
    }
</script>
