const axiosconfig = {
    baseurl: 'https://site.com/api/',
    timeout: 30000,
};

import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import {router} from '@/router';
import Dashboard from '@/component/dashboard/index';
import Layout from '@/component/layout/index';

import tempNav from '@/component/tempNav/index';

import BaerGS from '@/component/BaerGS/index';
import LoginForm from '@/component/login-form/index';

// include vue.js plugins
Vue.use(VueRouter);
Vue.use(BootstrapVue);



// include own vue.js components
Vue.component('Layout', Layout);
Vue.component('LoginForm', LoginForm);
Vue.component('tempNav', tempNav);

Vue.use(VueI18n)




const i18n = new VueI18n({
  locale: 'ru', // set locale
  messages: {
  en: {
    application: {
      baer: 'Baer-GS | Manage with Baer-GS | Go to Baer-GS'
    },
    login: {
      errLogin: 'Authorisation Error',
      title: 'Login',
      name: 'Your name: | Enter your name',
      password: 'Your password | Enter your password',
      comanyid: 'Your comany id | Enter your company id',
      rememberme: 'Remember Me',
      ok: 'Ok',
      cancel: 'Cancel'
    }
  },
  ru: {
    application: {
      baer: 'Baer-GS | Упаравление с Baer-GS | Перейти к Baer-GS'
    },
    login: {
      errLogin: 'Ошибка авторизации',
      title: 'Авторизация',
      name: 'Имя: | Введите имя',
      password: 'Пароль: | Введите пароль',
      comanyid: 'Идентификатор компании: | Введите номер компании',
      rememberme: 'Запомнить меня',
      ok: 'Подтвердить',
      cancel: 'Отмена'
    }
  }
} // set locale messages
})

const application = new Vue({
    router, i18n, el: ".application", data() {
      return {
        applications: []
      }
    },
    provide () {
        return {
            $i18n: i18n
        }
    }
});


application.i18n = i18n;
window.app = application;