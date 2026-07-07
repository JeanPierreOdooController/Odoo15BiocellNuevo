{
    'name': 'Ordenamiento de Guía de Remisión por Nombre de Producto',
    'version': '1.0',
    'author': 'ITGRUPO, Irving Llerena',
    'summary': 'Ordenamiento de productos por nombre en la Guía de Remisión',
    'description': """
        Módulo que modifica el reporte de Guía de Remisión para ordenar los productos por nombre dentro de cada paquete.
    """,
    'depends': ['biocell_pe_facturacion_electronica_despatch'],
    'data': [
        'views/report_despatch_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}