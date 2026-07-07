# -*- coding: utf-8 -*-
{
    'name': 'Segmento Ortobiológico',
    'version': '1.0',
    'description': 'Agrega segmento Ortobiológico y lo asocia a articulación de Medicina Deportiva',
    'author': 'ITGRUPO, Harold Portugal',
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
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True
}