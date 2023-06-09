# -*- coding: utf8 -*-
#
# Copyright (C) Cauly Kan, mail: cauliflower.kan@gmail.com
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from trac.core import Component, implements
from CategorizedFields import Category
from tracrpc.api import IXMLRPCHandler

class CategorizedFieldsRPC(Component):
    implements(IXMLRPCHandler)

    def __init__(self):
        pass

    def xmlrpc_namespace(self):
        return 'catfields'

    def xmlrpc_methods(self):
        yield 'WIKI_VIEW', ((dict,),), self.getCategories

    def getCategories(self, req):
        categories = {"_uncategorized": Category('_uncategorized', '')}
        categories['_uncategorized'].index = 0
        for opt_name, opt_value in self.config.options('categorized-fields'):
            if not '.' in opt_name:
                categories[opt_name] = Category(opt_name, opt_value)
            elif opt_name.split('.')[-1].startswith('hide_when_'):
                category_name, hide_condition = opt_name.split('.')
                categories[category_name].hide_condition.setdefault(hide_condition[len('hide_when_'):], []) \
                    .extend(filter(lambda x: x != '', opt_value.strip().split(',')))
            elif opt_name.split('.')[-1] == 'index':
                category_name = opt_name.split('.')[0]
                categories[category_name].index = int(opt_value)

        result = dict([(k, dict(v)) for k,v in categories.items()])

        return result
