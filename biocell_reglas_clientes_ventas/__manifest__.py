# -*- coding: utf-8 -*-
{
    'name': 'Sale Order - Partner No Create',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Deshabilita la creación de clientes desde el campo partner_id en pedidos de venta',
    'description': """
        Este módulo hereda la vista form de sale.order y agrega las opciones
        no_create y no_create_edit al campo partner_id para evitar la creación
        de nuevos clientes desde el pedido de venta.
    """,
    'author': 'ITGRUPO, Diego Aquino',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

