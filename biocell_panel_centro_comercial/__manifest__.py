# -*- encoding:utf-8 -*-
{
    'name': 'menu "Centro" en Configuracion-Ventas',
    'version': '1.0',
    'description': 'Modulo que crea vista tree,form del modelo account.analytic.journal',
    'author': 'ITGRUPO, Jhorel Revilla Calderon',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'biocell_meta_comercial',
        'biocell_devoluciones_comerciales_stock',
        'biocell_extensiones_contables'
    ],
    'data': [
        'views/menu.xml',
        'views/account_move.xml'
    ],
    'auto_install': False,
    'application': False
}