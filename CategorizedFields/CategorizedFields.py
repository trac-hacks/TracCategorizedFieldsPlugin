# -*- coding: utf8 -*-
#
# Copyright (C) Cauly Kan, mail: cauliflower.kan@gmail.com
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.


'''
Created on 2014-03-17

@author: cauly
'''
from trac.core import Component, implements, TracError
from trac.ticket import Ticket
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import ITemplateProvider, add_script, add_stylesheet
from genshi.filters.transform import Transformer, StreamBuffer
from genshi.builder import tag, Element
import time
import json
import datetime
import pkg_resources


class CategorizedFields(Component):
    implements(ITemplateStreamFilter, ITemplateProvider)

    # ITemplateProvider methods
    def get_htdocs_dirs(self):
        return [('CategorizedFields', pkg_resources.resource_filename('CategorizedFields', 'htdocs'))]

    def get_templates_dirs(self):
        return []

    # ITemplateStreamFilter
    def filter_stream(self, req, method, filename, stream, data):

        if filename != "ticket.html" and filename != 'ticket_preview.html':
            return stream

        if 'ticket' in data:

            add_script(req, 'CategorizedFields/js/bundle.js')
            add_stylesheet(req, 'CategorizedFields/css/base.css')

            ticket = data['ticket']

            self.categories = self.build_category()
            self.map_fields_to_category(self.categories)

            for index in list(self.categories.keys()):
                if self.category_is_hidden(self.categories[index], ticket):
                    del self.categories[index]

            cat_ticket = Element('cat-ticket', **{':categories': 'categories', ':ticket': 'ticket'})
            cat_modify = Element('cat-modify', **{':categories': 'categories', ':ticket': 'ticket'})
            
            stream |= Transformer('//div[@id="ticket"]').attr("id", "ticket1")
            stream |= Transformer('//div[@id="ticket1"]').after(tag.div(cat_ticket, id='ticket', class_='trac-content'))
            stream |= Transformer('//fieldset[@id="properties"]').attr("id", "properties1")
            stream |= Transformer('//fieldset[@id="properties1"]').after(tag.fieldset(cat_modify, id='properties'))
            
            stream |= Transformer('//body').append(tag.script("""
                            (function () {
                            var app1 = new Vue$({
                                el: '#ticket',
                                data: {
                                    categories: %s,
                                    ticket: %s,
                                }
                            });
                            var app2 = new Vue$({
                                el: '#properties',
                                data: {
                                    categories: %s,
                                    ticket: %s,
                                }
                            });
                            })(); 
                        """ % (json.dumps(self.categories, cls=CategoryEncoder),
                               json.dumps(ticket.values, cls=DateTimeJSONEncoder),
                               json.dumps(self.categories, cls=CategoryEncoder),
                               json.dumps(ticket.values, cls=DateTimeJSONEncoder))))

        return stream

    def build_category(self):
        '''
            build catagories from config

            e.g.
            [catagroy-fields]
            cat1 = category1
            cat1.hide_when_type = bug
            cat1.hide_when_status = new, closed 
        '''

        catagories = {"_uncategorized": Category('_uncategorized', '')}

        catagories['_uncategorized'].index = 0

        for opt_name, opt_value in self.config.options('categorized-fields'):

            if not '.' in opt_name:

                catagories[opt_name] = Category(opt_name, opt_value)

            elif opt_name.split('.')[-1].startswith('hide_when_'):

                category_name, hide_condition = opt_name.split('.')

                catagories[category_name].hide_condition.setdefault(hide_condition[len('hide_when_'):], []) \
                    .extend(filter(lambda x: x != '', opt_value.strip().split(',')))

            elif opt_name.split('.')[-1] == 'index':

                category_name = opt_name.split('.')[0]

                catagories[category_name].index = int(opt_value)

            elif opt_name.split('.')[-1] == 'noedit':

                category_name = opt_name.split('.')[0]

                catagories[category_name].noedit = opt_value == 'true'

        return catagories

    def map_fields_to_category(self, catagories):
        '''
            let's collect all custom fields and findout which fields do we have

            something like:

            [ticket-custom]
            test = text
            test.label = Test
            test.category = cat1
        '''

        categorized = []

        fields = ['reporter', 'summary', 'type', 'owner', 'priority', 'component', 'milestone', 'severity',
                       'keywords', 'cc', 'description']

        for opt_name, opt_value in self.config.options('ticket-custom'):

            if not '.' in opt_name and not opt_name in fields:

                fields.append(opt_name)

            elif opt_name.split('.')[-1] == 'category' and opt_value.strip() in catagories.keys():

                if not opt_name.split('.')[0] in catagories[opt_value].fields:

                    catagories[opt_value].fields.append(opt_name.split('.')[0])

                categorized.append(opt_name.split('.')[0])

        for item in self._sort_fields(fields):

            if not item in categorized and not item in catagories['_uncategorized'].fields:

                catagories['_uncategorized'].fields.append(item)

    def category_is_hidden(self, category, ticket):

        if category.name == '_uncategorized':
            return False

        for cond, list in category.hide_condition.items():

            if len(filter(lambda x: x['name'] == cond, ticket.fields)) == 1 and ticket[cond] in list:

                return True

        return False

    def _get_field_size(self, ticket, field_name):

        size = self.config.get('ticket-custom', '%s.display_size' % field_name, None)

        if (size != None and size in ['big', 'small']):

            return size

        else:

            return 'big' if filter(lambda x: x['name'] == field_name, ticket.fields)[0]['type'] == 'textarea' else 'small'

    def _sort_catagories(self, catagories):

        return sorted(catagories.values(), key=lambda x: x.index)

    def _sort_fields(self, fields):

        def foo(x):

            return self.config.getint('ticket-custom', x + '.index', 0)

        return sorted(fields, key=foo)


class Category(object):

    def __init__(self, name, display_name, noedit = False):

        self.name = name
        self.display_name = display_name
        self.hide_condition = {}
        self.fields = []
        self.index = 1
        self.noedit = noedit

    def __iter__(self):
        return self.__dict__.iteritems()


class CategoryEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return super(DateTimeJSONEncoder, self).default(obj)