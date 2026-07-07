# -*- coding: utf-8 -*-
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import time
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from openerp.osv import osv
import base64
from odoo import models, fields, api
import codecs
import subprocess
import sys
from datetime import datetime, timedelta

def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
	import openpyxl
except:
	install('openpyxl==3.0.5')

import openpyxl
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from openpyxl.styles.borders import Border, Side, BORDER_THIN
from openpyxl import Workbook
values = {}
from openpyxl.utils import get_column_letter
from openpyxl.cell import WriteOnlyCell

class product_template(models.Model):
	_inherit = 'product.template'

	check_unidad_especifica = fields.Boolean('Costeo x Unidad Especifica',default=False, tracking=1)


class stock_production_lot(models.Model):
	_inherit = 'stock.production.lot'

	precio_compra = fields.Float('Precio Compra',digits=(12,2), tracking=1)
	gasto_vinculado = fields.Float('Gasto Vinculado',digits=(12,2), tracking=1)
	precio_final = fields.Float('Precio Final',digits=(12,2), tracking=1)
	check_unidad_especifica = fields.Boolean(related='product_id.check_unidad_especifica')


