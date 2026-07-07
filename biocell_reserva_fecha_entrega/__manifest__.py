#-*- encoding: utf-8 -*-
{
    'name': 'Fecha de Entrega en Transferencias',
    'description': 'Modulo que agrega la fecha de entrega en transferencias',
    'author': 'ITGRUPO, Jhorel Revilla Calderon',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'sale_stock'
    ],
    'data': [
        'views/StockPicking.xml'
    ],
    'auto_install': False,
    'application': False
}