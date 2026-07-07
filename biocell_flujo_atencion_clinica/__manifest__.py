# -*- enconding:utf-8 -*-
{
    'name': 'Politica de Entrega-Informacion Clinica',
    'version': '1.0',
    'description': 'Modulo que crea el modelo de politica de entrega en informacion clinica.',
    'author': 'ITGRUPO, Jhorel Revilla Calderon',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'stock',
        'sale_stock',
        'biocell_meta_comercial',
        'biocell_datos_cliente_despacho'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/biocell_flujo_atencion_clinica.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml'
    ],
    'auto_install': False,
    'application': False
}