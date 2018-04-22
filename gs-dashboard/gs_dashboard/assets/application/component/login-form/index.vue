<template>
<div>
  <b-link v-b-modal.modal1>{{ $t("login.title") }}</b-link>
  <!-- Modal Component-->
  <b-modal id="modal1" ref="modal1" :title="$t('login.title')" hide-footer centered size="sm">

<!--<button @click="setLang('en')">en</button><button @click="setLang('ru')">ru</button>-->

<b-form @submit="onSubmit" @reset="onReset" v-if="show">
          <b-alert show variant="warning" v-if="form.errShow">
              {{ $t("login.errLogin") }}
          </b-alert>
         <b-form-group id="loginInputGroup1"
                    :label="$tc('login.name', 1)"
                    label-for="InputGroup1"
                    autofocus>
        <b-form-input id="loginInputGroup1"
                      type="text"
                      v-model="form.name"
                      required
                      :placeholder="$tc('login.name', 2)">
        </b-form-input>
      </b-form-group>

      <b-form-group id="loginInputGroup2"
                     :label="$tc('login.password', 1)"
                    label-for="InputGroup2">
        <b-form-input id="InputGroup2"
                      type="password"
                      v-model="form.password"
                      required
                      :placeholder="$tc('login.password', 2)">
        </b-form-input>
      </b-form-group>

        <b-form-group id="loginInputGroup3"
                    :label="$tc('login.comanyid', 1)"
                    label-for="InputGroup3">
        <b-form-input id="InputGroup3"
                      type="number"
                      min="1"
                      v-model="form.companyid"
                      required
                      :placeholder="$tc('login.comanyid', 2)">
        </b-form-input>
      </b-form-group>
 
        <b-form-group>
          <b-form-checkbox id="InputGroup4" 
                       v-model="form.checked"
                       value="accepted"
                       unchecked-value="not_accepted">
                            {{ $t("login.rememberme") }}
          </b-form-checkbox>
        </b-form-group>

       <input type="checkbox" class="custom-control-input" name="" >

        <b-row align-h="around">
              <b-button class="col-sm-5" type="submit" variant="primary">{{ $t("login.ok") }}</b-button>
              <b-button class="col-sm-5" type="reset" variant="danger">{{ $t("login.cancel") }}</b-button>
        </b-row>

    </b-form>

  </b-modal>
</div>
</template>



<script>
import axios from 'axios';

export default {

inject: ['$i18n'],
  data () {

    return {
      form: {
        name: '',
        password: '',
        companyid: '',
        checked: 'accepted',
        errShow: false
      },
       show: true,
       response: ''
    
    }
  },
  methods: {
    setLang: function (lng) {
      app.i18n.locale = lng;
    },
    onSubmit (evt) {
      evt.preventDefault();
        axios.post('/authorization', JSON.stringify(this.form)).then(response => {
        this.$root.applications = response.data;
        if (response.data[0]) {
          this.$refs.modal1.hide()
        } else{
          this.form.errShow = true
        }
      });
      },
    onReset (evt) {
      evt.preventDefault();
      /* Reset our form values */
      this.form.name = '';
      this.form.password = '';
      this.form.companyid = '';
      this.form.checked = [];
      /* Trick to reset/clear native browser form validation state */
      this.show = false;
      this.$nextTick(() => { this.show = true });
    }
  },
  mounted() {
    this.$i18n.locale = (navigator.language || navigator.systemLanguage || navigator.userLanguage).substr(0, 2).toLowerCase();
;
  }
}
</script>
<style>
#InputGroup3 { 
  -moz-appearance: textfield;
}
#InputGroup3::-webkit-inner-spin-button { 
  display: none;
}
</style>