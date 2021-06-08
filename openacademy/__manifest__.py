# -*- coding: utf-8 -*-
# {
#     'name': "openacademy",

#     'summary': """
#         Short (1 phrase/line) summary of the module's purpose, used as
#         subtitle on modules listing or apps.openerp.com""",

#     'description': """
#         Long description of module's purpose
#     """,

#     'author': "My Company",
#     'website': "http://www.yourcompany.com",

#     # Categories can be used to filter modules in modules listing
#     # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
#     # for the full list
#     'category': 'Uncategorized',
#     'version': '0.1',

#     # any module necessary for this one to work correctly
#     'depends': ['base'],

#     # always loaded
#     'data': [
#         # 'security/ir.model.access.csv',
#         # 'views/views.xml',
#         'views/templates.xml',
#     ],
#     # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
# }

{
    'name' : 'openacademy',
    'version' : '1.0',
    'summary': 'Open Academy',
    'sequence': -10,
    'description': """
    Open Academy
    """,
    'category': 'Uncategorized',
    'website': 'http://www.yourcompany.com',
    'depends' : ['base','sale','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/mail_template.xml',
        'views/views.xml',
        'views/teacher.xml',
        'views/course.xml',
        'reports/custom_header_footer.xml',
        'reports/report.xml',
        'reports/student_card.xml',
        'reports/teacher_card.xml',
        'reports/course_report.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
