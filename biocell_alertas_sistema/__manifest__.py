# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'LLIKHA NOTIFICATION',
    'summary': 'Notificaciones',
    'category': 'All',
    'author':'LLIKHA-BO',
    'description': """Notificationes
    """,
    'depends': ['account_accountant','web'],
    'qweb': [    
        'static/src/js/export_file_manager_tmpl.xml',
        'static/src/js/notification_button.xml',        
    ],
    'assets': {
        'web.assets_common': [
            'biocell_alertas_sistema/static/src/js/action_manager_notify.js',
            'biocell_alertas_sistema/static/src/js/styles.css',
        ],
        'web.assets_backend': [
            'biocell_alertas_sistema/static/src/js/actions.js',
        ],        
    },
    'auto_install': False,
    'installable': True,
}
