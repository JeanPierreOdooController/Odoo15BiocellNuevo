# -*- encoding: utf-8 -*-
{
    'name': 'Bloquear Transferencias por producto y lote',
    'category': 'Inventory',
    'author': 'ITGRUPO, Harold Portugal',
    'depends': ['stock', 'product'],
    'version': '1.0',
    'description':"""Bloquea validación de transferencias si producto o lote están bloqueados
    """,
    'auto_install': False,
    'demo': [],

    'data': [
        "security/res_groups.xml",
        "views/product_template_views.xml",
        "views/stock_production_lot_views.xml",
        ],
    'installable': True
}