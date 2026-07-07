# -*- coding: utf-8 -*-
{
    'name': 'Ventas envio a api',
    'version': '1.0',
    'description': 'Módulo de envio a api de ventas',
    'author': 'ITGRUPO',
    'license': 'LGPL-3',
    'depends': [
        'biocell_conector_ventas',
        'biocell_devoluciones_comerciales_stock',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True
}