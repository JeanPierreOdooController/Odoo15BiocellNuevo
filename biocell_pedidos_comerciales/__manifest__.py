# -*- coding: utf-8 -*-
{
    'name': 'Articulaciones para el Segmento Trauma / M.D.',
    'version': '1.0',
    'description': 'Agrega opciones seleccionables de articulación para el segmento Trauma o¿/ M.D.',
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