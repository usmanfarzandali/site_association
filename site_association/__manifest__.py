# -*- coding: utf-8 -*-
{
    'name': "Site Association - NZ",

    'summary': """
        Changed the dependency and character field of employees, create the record of member through website
        form""",

    'description': """
        Long description of module's purpose
    """,

    'author': "NZ",
    'website': "http://www.nidazehra.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','website','membership'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/website_form.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
