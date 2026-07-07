# -*- coding: utf-8 -*-
{
    'name': 'Ventas envio a api',
    'version': '1.0',
    'description': 'Módulo de envio a api de ventas',
    'author': 'ITGRUPO, Irving Llerena',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'sale_management',
        'stock',
        'account',
        'biocell_control_bultos',
        'biocell_meta_comercial',
        'biocell_flujo_atencion_clinica',
        'biocell_devoluciones_comerciales_stock',
        'biocell_confirmacion_recepcion_mercaderia',
        'biocell_herramientas_tributarias_4',
        'biocell_pe_facturacion_electronica',
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'biocell_conector_ventas/static/src/js/confirm_sugery_date.js',
        ],
    },
    'auto_install': False,
    'application': False,
    'installable': True
}
