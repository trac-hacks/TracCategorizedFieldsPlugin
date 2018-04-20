<template>
    <div>
        <legend v-html="getTicketHeader()"></legend>
        <div v-for="name in getCategories()" :key="name">
            <div v-if="name != '_uncategorized'" class="edit_category_header">{{categories[name].display_name}}</div>
            <table class="edit_category">
                <tbody>
                    <tr v-for="row in getCategoryRows(name)">
                        <th :id="'label_' + row.name" v-html="getHtml(row.header)" class="col1"></th>
                        <td :id="'edit_' + row.name" v-html="getHtml(row.field)" :colspan="getColspan(row)" :class="{col1: !row.fullrow, fullrow: row.fullrow}"></td>
                        <th :id="'label_' + row.name2" v-html="getHtml(row.header2)" v-if="!row.fullrow" class="col2"></th>
                        <td :id="'edit_' + row.name2" v-html="getHtml(row.field2)" v-if="!row.fullrow" class="col2"></td>
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
            this.element = $("#properties1");
            for (catindex in this.categories) {
                this.categories[catindex].fields.forEach(fieldName => {
                    var header = this.element.find('label[for="field-' + fieldName + '"]');
                    if (header.length > 0) {
                        this.headers[fieldName] = header;
                        this.fields[fieldName] = null;
                        var field = this.element.find('#field-' + fieldName).parent();
                        if (field.length > 0) {
                            this.fields[fieldName] = field;
                        }
                    }
                });
            }
            $('#properties1').detach();
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
                return this.element.children("legend").html();
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
                    if (field == 'description' || this.fields[field] && this.fields[field].parent().attr('colspan') == 3) {
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
                return element ? element.parent().attr('class') : '';
            },
            getHtml: function (element) {
                return element ? element.html() : '';
            }
        }
    }
</script>