# -*- coding: utf8 -*-
#
# Copyright (C) Cauly Kan, mail: cauliflower.kan@gmail.com
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.


'''
Created on 2014-03-12

@author: cauly
'''
from setuptools import find_packages, setup

setup(
    name='TracCategorizedFields', version='2.0.1',
    packages=find_packages(exclude=['*.tests*']),
    license="BSD 3-Clause",
    author_email='cauliflower.kan@gmail.com',
    author='Cauly Kan',
    classifiers=[
            'Framework :: Trac',
            'Programming Language :: Python :: 2.7',
        ],
    package_data={ 'CategorizedFields': ['htdocs/js/*.js', 'htdocs/images/*.png', 'htdocs/css/*.css', 'templates/*.html'] },
    entry_points={
        'trac.plugins': [
            'traccategorizedfields = CategorizedFields',
        ],
    },
)
