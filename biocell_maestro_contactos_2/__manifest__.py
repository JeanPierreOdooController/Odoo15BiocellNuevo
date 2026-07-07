# -*- coding: utf-8 -*-
{
    'name': 'Partner & Sale Custom Vendedores',
    'version': '1.0',
    'description': 'Agrega campos de vendedor personalizado a biocell_directorio_contactos y ventas',
    'author': 'ITGRUPO, Harold Portugal',
    'license': 'LGPL-3',
    'depends': [
        "base",
        "sale",
        "account",
        "biocell_directorio_contactos",
        "biocell_panel_analisis_ventas",
        "biocell_meta_comercial",
        "biocell_conector_ventas"
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/account_move.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True
}