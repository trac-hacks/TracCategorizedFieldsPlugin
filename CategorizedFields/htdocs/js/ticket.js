import Vue from 'vue';
import ticket from './ticket.vue';
import modify from './modify.vue';

window.Vue$ = Vue;

Vue$.component('cat-ticket', ticket);
Vue$.component('cat-modify', modify);
