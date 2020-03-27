import Vue from 'vue';
import ticket from './ticket.vue';
import modify from './modify.vue';

window.Vue$ = Vue;

Vue$.component('cat-ticket', ticket);
Vue$.component('cat-modify', modify);

$(document).ready(function () {
    var cat = JSON.parse(window.categorizedFieldsData.categories);
    var t = JSON.parse(window.categorizedFieldsData.ticket);

    //$("#ticket").attr("id", "ticket1");
    $(".properties").attr("id", "ticket-properties1");
    $("#ticket-properties1").after($("<div id='ticket-properties'><table class='properties'><cat-ticket :categories='categories' :ticket='categories'></cat-ticket></table></div>"));
    $("#properties").attr("id", "properties1");
    $("#properties1").after($("<fieldset id='properties'><cat-modify :categories='categories' :ticket='categories'></cat-modify></fieldset>"));

    window.app1 = new Vue$({
        el: '#ticket-properties',
        data: {
            categories: cat,
            ticket: t,
        }
    });
    window.app2 = new Vue$({
        el: '#properties',
        data: {
            categories: cat,
            ticket: t,
        }
    });
});
