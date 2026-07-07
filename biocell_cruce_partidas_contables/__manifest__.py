# -*- encoding: utf-8 -*-
{
	'name': 'Account Reconcile IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables'],
	'version': '1.0',
	'description':"""
		- Modulo para agregar Tipo de Documento y Numero de Comprobante a las lineas de Asiento Generadas en la Conciliacion
		- Conciliacion especial para asientos de apertura y cierre
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		#'views/assets.xml',
		#'views/account_reconcile_model.xml'
	],
	'installable': True,
	'license': 'LGPL-3',
    'assets': {
        'web.assets_qweb': [
            'biocell_cruce_partidas_contables/static/src/xml/**/*',
        ],
    }
}
