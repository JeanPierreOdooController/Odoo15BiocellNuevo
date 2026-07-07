# -*- encoding: utf-8 -*-
{
	'name': 'Campo Trabajador en gastos ',
	'version': '1.0',
	'description': 'COTIZADO Desarrollo con costo: Campo Trabajador en gastos (#21373)',
	'author': 'ITGRUPO, Sebastian Moises Loraico Lopez',
	'license': 'LGPL-3',
	'category': '',
	'depends': [
		'biocell_extensiones_contables','biocell_registro_operaciones_diarias'
	],
	'data': [
		'views/account_move.xml',
        'views/account_book_diary_view.xml',
	],	
	'auto_install': False,
	'application': False,	
}