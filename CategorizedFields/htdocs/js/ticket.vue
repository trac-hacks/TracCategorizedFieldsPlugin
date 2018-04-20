<template>
    <div>
        <div v-html="getTicketHeader()"></div>
        <div v-for="name in getCategories()" :key="name" :id="'cat_' + name" :class="{description: name != '_uncategorized'}">
            <h3 v-if="name != '_uncategorized'">{{categories[name].display_name}}</h3>
            <table class="properties" style="border-top: none;">
                <tbody>
                    <tr v-for="row in getCategoryRows(name)" :class="{fullrow: row.fullrow}">
                        <th :id="'h_' + row.name" v-html="getHtml(row.header)" :class="getClass(row.header)"></th>
                        <td :headers="'h_' + row.name" v-html="getHtml(row.field)" :colspan="getColspan(row)" :class="getClass(row.field)"></td>
                        <th :id="'h_' + row.name2" v-html="getHtml(row.header2)" v-if="!row.fullrow" :class="getClass(row.header2)"></th>
                        <td :headers="'h_' + row.name2" v-html="getHtml(row.field2)" v-if="!row.fullrow" :class="getClass(row.field2)"></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
    module.exports = {
        props: ['categories', 'ticket'],
        created: function () {
            this.element = $("#ticket1");
            for (catindex in this.categories) {
                this.categories[catindex].fields.forEach(fieldName => {
                    var header = this.element.find('th#h_' + fieldName);
                    if (header.length > 0) {
                        this.headers[fieldName] = header;
                        this.fields[fieldName] = null;
                        var field = header.siblings('td[headers=h_' + fieldName + ']');
                        if (field.length > 0) {
                            this.fields[fieldName] = field;
                        }
                    }
                });
            }
            $('#ticket1').detach();
        },
        data: function () {
            return {
                headers: {},
                fields: {},
                element: null,
            };
        },
        methods: {
            getTicketHeader: function () {
                return this.element.children("div.date").detach().wrap('<p/>').parent().html() +
                    this.element.children("h2").detach().wrap('<p/>').parent().html() +
                    this.element.children("h1").detach().wrap('<p/>').parent().html();
            },
            getCategories: function () {
                return Object.keys(this.categories).sort((a, b) => this.categories[a].index - this.categories[b].index);
            },
            getCategoryRows: function (name) {
                var category = this.categories[name];
                var returnLine = true;
                var result = [];

                for (i in category.fields) {
                    field = category.fields[i];
                    if (field == 'summary') {
                        continue;
                    }
                    if (this.fields[field] && this.fields[field].attr('colspan') == 3) {
                        result.push({ header: this.headers[field], field: this.fields[field], name: field, fullrow: true });
                        returnLine = true;
                    } else {
                        if (this.headers[field]) {
                            if (returnLine) {
                                result.push({ header: this.headers[field], field: this.fields[field], name: field, fullrow: false });
                                returnLine = false;
                            } else {
                                result[result.length - 1]['header2'] = this.headers[field];
                                result[result.length - 1]['field2'] = this.fields[field];
                                result[result.length - 1]['name2'] = field;
                                returnLine = true;
                            }
                        }
                    }
                }

                return result;
            },
            getColspan: function (row) {
                return row.fullrow ? 3 : '';
            },
            getClass: function (element) {
                return element ? element.attr('class') : '';
            },
            getHtml: function (element) {
                return element ? element.html() : '';
            }
        }
    }
</script>