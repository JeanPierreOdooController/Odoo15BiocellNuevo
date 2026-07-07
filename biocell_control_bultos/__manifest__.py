{
    'name': 'Biocell Paquete',
    'version': '1.0',
    'description': 'Paquete',
    'author': 'ITGRUPO',
    'license': 'LGPL-3',
    'category': 'Stock',
    'auto_install': False,
    'depends': [
        'stock',
        'sale_stock'
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/button.xml',
    ],
    'installable': True
}
