{
    'name': 'reporte biocel paquete',
    'version': '1.0',
    'description': 'reporte biocel paquete',
    'author': 'ITGRUPO',
    'license': 'LGPL-3',
    'category': 'Stock',
    'auto_install': False,
    'depends': [
        'stock',
        'biocell_control_bultos'
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/button.xml',
    ],
    'installable': True
}