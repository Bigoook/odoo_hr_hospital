{
    'name': 'HR Hospital',
    'summary': 'HR Hospital',
    'author': 'big_ooo',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'LGPL-3',
    'version': '19.0.2.0.0',
    'depends': [
        'base',
        'web',
    ],
    'external_dependencies': {
        'python': [],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': ['static/description/icon.png'],
    'data': [
        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_hospital_security.xml',
        'data/hr_hospital_disease_data.xml',
        'data/hr_hospital_doctor_category_data.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_doctor_category_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_doctor_history_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_visit_views.xml',
        'report/hr_hospital_doctor_report_views.xml',
        'wizards/hr_hospital_mass_reassign_doctor_wizard_views.xml',
        'wizards/hr_hospital_visit_report_wizard_views.xml',
        'wizards/hr_hospital_disease_report_wizard_views.xml',
        'views/hr_hospital_menu.xml',
    ],

    'assets': {
        'web.report_assets_common': [
            'hr_hospital/static/src/scss/hr_hospital_doctor_report.scss',
        ],
    },

    'demo': [
        'demo/hr_hospital_demo.xml',
        'demo/hr_hospital_doctor_history_demo.xml',
        'demo/hr_hospital_disease_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
    ],
}
