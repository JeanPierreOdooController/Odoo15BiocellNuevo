# -*- encoding: utf-8 -*-
{
	'name': 'Kardex Actualizar Transferencias Internas IT',
	'version': '1.0',
	'author': 'ITGRUPO-KARDEX',
	'website': '',
	'category': 'account',
	'depends': ['biocell_kardex_costeo_existencias','biocell_bloqueo_inventario_valorizado'],
	'description': """Actualizador de Transferencias Internas el valor unitario""",
	'demo': [],
	'data': [
        'security/ir.model.access.csv',
		'stock_move_view.xml',
	],
	'auto_install': False,
	'installable': True
}

