# -*- encoding: utf-8 -*-
{
	'name': 'Reporte de Detalle de Ingreso y salida',
	'category': 'stock',
	'author': 'ITGRUPO, Sebastian Moises Loraico Lopez',
	'depends': ['biocell_kardex_contabilizacion_existencias_2'],
	'version': '1.0',
	'description':"""
	- Detalle de Movimientos en Asientos Contables
	""",
	'auto_install': False,
	'demo': [],
	"data": [
        "views/kardex_entry_income_book_views.xml",
        "views/kardex_entry_outcome_book_views.xml"
    ],
	'installable': True,
	'license': 'LGPL-3'
}
