from odoo import models, fields, api
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.exceptions import UserError
import base64


class horas_hombre_import(models.TransientModel):
	_name = "importador.moves.lines"
	_description = "Importador Movimientos De Almacen"

	name = fields.Char(string="Nombre Archivo",default="new.xls")
	file = fields.Binary(string='Archivo')
	stock_picking_id=fields.Many2one("stock.picking",string="Albaran",required=True)
	import_product_type = fields.Selection([('create','Crear Registros'),('update','Actualizar Registros')],string='Tipo de Operacion', required=True,default="create")
	company_id = fields.Many2one('res.company',string=u'Compañia',required=True, default=lambda self: self.env.company,readonly=True)
	warning = fields.Char(string="Advertencia",compute="get_ad")
	mensaje_formato = fields.Char(string="Formato De Archivo",readonly=True)
	errores_txt = fields.Text(string="Errores")


	@api.depends("import_product_type")
	def get_ad(self):
		for i in self:
			if i.import_product_type=='create':
				i.warning=False
			else:
				i.warning="Advertencia, El Actualizar Eliminara Los Movimientos(Operaciones Detalladas) Existentes Para Reemplazarlos Por Los Nuevos Ingresados"
 
 
 
 
	def get_read_lotes(self):
		for l in self:
			if l.import_product_type=='create':
				if not self.file:
					raise UserError("Debe cargar un archivo de importación.")
				if "." in self.name:
					if self.name.split(".")[1]!="csv":
						if self.name.split(".")[1]!="txt":
							raise UserError("Debes Subir Un Archivo De Texto(.txt) O .csv")
				#if self.stock_picking_id.picking_type_id.code == 'incoming':
				if self.stock_picking_id.location_id.usage=='supplier' and self.stock_picking_id.location_dest_id.usage=='internal':
					data = base64.b64decode(self.file).decode('utf-8')
					info = data.split('\n')
					cont = 0
					verificacion_lotes = []
					contenedor_lotes = {}
					errores = ""
					for i in info:
						data_linea = i.split(';')
						if len(data_linea)==5:
							verificacion_lotes.append( (data_linea[0].strip(),data_linea[1].strip()))
							producto = self.env['product.product'].search([(l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
							if len(producto)>0:
								existe_lote = self.env['stock.production.lot'].search([('name','=',data_linea[1].strip()),('product_id.'+l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
								if len(existe_lote)>0:
									if not ("Lote Ya Existente para el producto seleccionado: (" + data_linea[0].strip()+ "," + data_linea[1].strip() + ")\n") in errores:
										errores += "Lote Ya Existente para el producto seleccionado: (" + data_linea[0].strip()+ "," + data_linea[1].strip() + ")\n"
								key_imp = None
								if producto[0].tracking == 'lot':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if producto[0].tracking == 'serial':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if producto[0].tracking == 'none':
									if data_linea[1].strip()!='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if key_imp in contenedor_lotes:
									detalle_lotes = contenedor_lotes[key_imp]
									detalle_lotes.append(data_linea)
									contenedor_lotes[key_imp] = detalle_lotes
								else:
									contenedor_lotes[key_imp] = [data_linea]
							else:
								if ("No existe el producto: " + data_linea[0].strip() + "\n" ) in errores:
									pass
								else:
									errores += "No existe el producto: " + data_linea[0].strip()  + "\n"
						else:
							if len(data_linea)!=1:
								if not ("Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea)) in errores:
									errores += "Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea) + "\n"
					self.errores_txt = errores

					if errores !="":
						raise UserError(str(errores))

	

					error_new = ""
					for mat in contenedor_lotes:
						#C310|0E0VHV|67|01/18/2020|78.76|
						for elem in contenedor_lotes[mat]:
							if self.env['product.product'].browse(mat[0]).tracking == 'lot':
								elem_move_picking = self.env['stock.move'].sudo().search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)!=0:
									if len(elem_move_picking)>1:
										raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
									if len(elem_move_picking)==1:
										if len(elem_move_picking)==1:
											elem_move_picking.sudo().price_unit_it = float(elem[4])
											move_line_vals = {
												'picking_id': self.stock_picking_id.id,
												'location_dest_id': self.stock_picking_id.location_dest_id.id,
												'location_id': self.stock_picking_id.location_id.id,
												'product_id': elem_move_picking.product_id.id,
												'product_uom_id': elem_move_picking.product_uom.id,
												'qty_done': float(elem[2]),
												'package_level_id':False,
												'move_id':elem_move_picking.id,
												'lot_name':str(elem[1])
											}
											self.env['stock.move.line'].create(move_line_vals)

							elif self.env['product.product'].browse(mat[0]).tracking == 'serial':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if elem[2] != "1":
									if not ("Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])) in error_new:
										error_new = error_new + "Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])+"\n"
								if len(elem_move_picking)==1:
									move_line_repetido_serial = self.env['stock.move.line'].search([('picking_id','=',self.stock_picking_id.id),('move_id','=',elem_move_picking.id),('product_id','=',elem_move_picking.product_id.id),('lot_name','=',str(elem[1]))])
									if len(move_line_repetido_serial)>0:
										if not ("Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])) in error_new:
											error_new = error_new + "Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])+"\n"
									elem_move_picking.sudo().price_unit_it = float(elem[4])
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_name':str(elem[1])
									}
									self.env['stock.move.line'].create(move_line_vals)


							elif self.env['product.product'].browse(mat[0]).tracking == 'none':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)==1:
									elem_move_picking.sudo().price_unit_it = float(elem[4])
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_name':str(elem[1])
									}
									self.env['stock.move.line'].create(move_line_vals)
					self.stock_picking_id.refresh()
					self.stock_picking_id.move_line_ids_without_package.refresh()
					if error_new != '':
						raise UserError(str(error_new))
					revision_final = ""
					for moves in self.stock_picking_id.move_ids_without_package:
						if moves.quantity_done > moves.product_uom_qty:
							if not ("Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)) in revision_final:
								revision_final = revision_final + "Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)+"\n"
					if revision_final!="":
						raise UserError(str(revision_final))
				else:
					data = base64.b64decode(self.file).decode('utf-8')
					info = data.split('\n')
					cont = 0
					verificacion_lotes = []
					contenedor_lotes = {}
					errores = ""
					for i in info:
						data_linea = i.split(';')
						if len(data_linea)==5:
							verificacion_lotes.append(data_linea[1].strip())                    

							producto = self.env['product.product'].search([(l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
							if len(producto)>0:
								existe_lote = self.env['stock.production.lot'].search([('name','=',data_linea[1].strip()),('product_id.'+l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
								if len(existe_lote)==0 or len(existe_lote)>1 :
									if data_linea[1].strip() != "":
										errores += "No existe el lote para el producto seleccionado: (" + data_linea[0].strip()+ "," + data_linea[1].strip() + ")\n"
								key_imp = None
								if producto[0].tracking == 'lot':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,existe_lote.id)
								if producto[0].tracking == 'serial':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,existe_lote.id)
								if producto[0].tracking == 'none':
									if data_linea[1].strip()!='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if key_imp in contenedor_lotes:
									detalle_lotes = contenedor_lotes[key_imp]
									detalle_lotes.append(data_linea)
									contenedor_lotes[key_imp] = detalle_lotes
								else:
									contenedor_lotes[key_imp] = [data_linea]
							else:
								if ("No existe el producto: " + data_linea[0].strip() + "\n" ) in errores:
									pass
								else:
									errores += "No existe el producto: " + data_linea[0].strip()  + "\n"
						else:
							if len(data_linea)!=1:
								if not ("Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea)) in errores:
									errores += "Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea) + "\n"
					self.errores_txt = errores

					if errores != "":
						raise UserError(str(errores))
					lines_updated=[]
					error_new = ""
					for mat in contenedor_lotes:
						#C310|0E0VHV|67|01/18/2020|78.76|
						for elem in contenedor_lotes[mat]:
							lote = False
							existelote = False
							if mat[1]!=False:
								existelote = self.env['stock.production.lot'].search([('id','=',mat[1])])
								if len(existelote)==0 or len(existelote)>1:
									error_new += "No existe el lote para el producto seleccionado: (" + elem[0].strip()+ "," + elem[1].strip() + ")\n"
								else:
									lote = existelote.id
							if self.env['product.product'].browse(mat[0]).tracking == 'lot':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)!=0:
									if len(elem_move_picking)>1:
										raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
									if len(elem_move_picking)!=0:
										if len(elem_move_picking)==1:
											move_line_vals = {
												'picking_id': self.stock_picking_id.id,
												'location_dest_id': self.stock_picking_id.location_dest_id.id,
												'location_id': self.stock_picking_id.location_id.id,
												'product_id': elem_move_picking.product_id.id,
												'product_uom_id': elem_move_picking.product_uom.id,
												'qty_done': float(elem[2]),
												'package_level_id':False,
												'move_id':elem_move_picking.id,
												'lot_id':lote
											}
											self.env['stock.move.line'].create(move_line_vals)

							elif self.env['product.product'].browse(mat[0]).tracking == 'serial':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if elem[2] != "1":
									if not ("Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])) in error_new:
										error_new = error_new + "Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])+"\n"
								if len(elem_move_picking)==1:
									move_line_repetido_serial = self.env['stock.move.line'].search([('picking_id','=',self.stock_picking_id.id),('move_id','=',elem_move_picking.id),('product_id','=',elem_move_picking.product_id.id),('lot_id','=',lote)])
									if len(move_line_repetido_serial)>0:
										if not ("Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])) in error_new:
											error_new = error_new + "Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])+"\n"
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_id':lote
									}
									self.env['stock.move.line'].create(move_line_vals)


							elif self.env['product.product'].browse(mat[0]).tracking == 'none':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)==1:
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_id':lote
									}
									self.env['stock.move.line'].create(move_line_vals)
					if error_new!="":
						raise UserError(str(error_new))
					revision_final = ""
					for moves in self.stock_picking_id.move_ids_without_package:
						if moves.quantity_done > moves.product_uom_qty:
							if not ("Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)) in revision_final:
								revision_final = revision_final + "Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)+"\n"
					if revision_final!="":
						raise UserError(str(revision_final))

			else:
				#ACTUALIZAR
				stock_moves_ya_limpios = []
				if not self.file:
					raise UserError("Debe cargar un archivo de importación.")
				#if self.stock_picking_id.picking_type_id.code == 'incoming':
				if self.stock_picking_id.location_id.usage=='supplier' and self.stock_picking_id.location_dest_id.usage=='internal':
					data = base64.b64decode(self.file).decode('utf-8')
					info = data.split('\n')
					cont = 0
					verificacion_lotes = []
					contenedor_lotes = {}
					errores = ""
					for i in info:
						data_linea = i.split(';')
						if len(data_linea)==5:
							verificacion_lotes.append( (data_linea[0].strip(),data_linea[1].strip()) )                    

							producto = self.env['product.product'].search([(l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
							if len(producto)>0:
								existe_lote = self.env['stock.production.lot'].search([('name','=',data_linea[1].strip()),('product_id.'+l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
								if len(existe_lote)>0:
									if not ("Lote Ya Existente para el producto seleccionado: (" + data_linea[0].strip()+ "," + data_linea[1].strip() + ")\n") in errores:
										errores += "Lote Ya Existente para el producto seleccionado: (" + data_linea[0].strip()+ "," + data_linea[1].strip() + ")\n"
								key_imp = None
								if producto[0].tracking == 'lot':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if producto[0].tracking == 'serial':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if producto[0].tracking == 'none':
									if data_linea[1].strip()!='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if key_imp in contenedor_lotes:
									detalle_lotes = contenedor_lotes[key_imp]
									detalle_lotes.append(data_linea)
									contenedor_lotes[key_imp] = detalle_lotes
								else:
									contenedor_lotes[key_imp] = [data_linea]
							else:
								if ("No existe el producto: " + data_linea[0].strip() + "\n" ) in errores:
									pass
								else:
									errores += "No existe el producto: " + data_linea[0].strip()  + "\n"
						else:
							if len(data_linea)!=1:
								if not ("Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea)) in errores:
									errores += "Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea) + "\n"
					self.errores_txt = errores

					if errores !="":
						raise UserError(str(errores))

	#revisar				if l.stock_picking_id.state == 'draft':

	#					for elem in contenedor_lotes:
							#C310|0E0VHV|67|01/18/2020|78.76
	#						data = {
	#							'product_id':elem,
	#							'product_uom_qty':len(contenedor_lotes[elem]) if self.env['product.product'].browse(elem[0]).tracking == 'serial' else float(contenedor_lotes[elem][0][2]),
	#							'name':self.env['product.product'].browse(elem[0]).name,
	#							'product_uom':self.env['product.product'].browse(elem[0]).uom_id.id,
	#							'location_id':self.stock_picking_id.location_id.id,
	#							'location_dest_id':self.stock_picking_id.location_dest_id.id,
	#							'picking_type_id':self.stock_picking_id.picking_type_id.id,
	#							'price_unit_it':float(contenedor_lotes[elem][0][4].strip()) if contenedor_lotes[elem][0][4].strip() != "" else 0,
	#						}
	#						self.stock_picking_id.write({'move_ids_without_package':[(0,0,data)]})
	#Revisar					l.stock_picking_id.action_confirm()

	#					for lineas_eliminanr in self.move_line_ids_without_package:
	#						if lineas_eliminanr.tracking == 'serial':
	#							lineas_eliminanr.unlink()
	#						elif lineas_eliminanr.tracking == 'lot':
	#							lineas_eliminanr.unlink()
	#						elif lineas_eliminanr.tracking == 'none':
	#							lineas_eliminanr.unlink()
						
	#					for i in self.stock_picking_id.move_ids_without_package:
	#						if i.product_id.tracking == 'serial':
	#							data = {
	#								'product_id':i.product_id.id,
	#								'move_id':i.id,
	#								'next_serial_count':i.product_uom_qty,
	#								'next_serial_number':1,
	#							}
	#							obj_tmp = self.env['stock.assign.serial'].create(data)
	#							obj_tmp.generate_serial_numbers()

					error_new = ""
					for mat in contenedor_lotes:
						#C310|0E0VHV|67|01/18/2020|78.76|
						for elem in contenedor_lotes[mat]:
							if self.env['product.product'].browse(mat[0]).tracking == 'lot':
								elem_move_picking = self.env['stock.move'].sudo().search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)!=0:
									if len(elem_move_picking)>1:
										raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
									if len(elem_move_picking)==1:
										if len(elem_move_picking)==1:
											if not (elem_move_picking.id) in stock_moves_ya_limpios:
												for eliminar_moves in elem_move_picking.move_line_ids:
													eliminar_moves.sudo().unlink()
												stock_moves_ya_limpios.append(elem_move_picking.id)
											elem_move_picking.sudo().price_unit_it = float(elem[4])
											move_line_vals = {
												'picking_id': self.stock_picking_id.id,
												'location_dest_id': self.stock_picking_id.location_dest_id.id,
												'location_id': self.stock_picking_id.location_id.id,
												'product_id': elem_move_picking.product_id.id,
												'product_uom_id': elem_move_picking.product_uom.id,
												'qty_done': float(elem[2]),
												'package_level_id':False,
												'move_id':elem_move_picking.id,
												'lot_name':str(elem[1])
											}
											self.env['stock.move.line'].create(move_line_vals)

							elif self.env['product.product'].browse(mat[0]).tracking == 'serial':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if elem[2] != "1":
									if not ("Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])) in error_new:
										error_new = error_new + "Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])+"\n"
								if len(elem_move_picking)==1:
									if not (elem_move_picking.id) in stock_moves_ya_limpios:
										for eliminar_moves in elem_move_picking.move_line_ids:
											eliminar_moves.sudo().unlink()
										stock_moves_ya_limpios.append(elem_move_picking.id)
									move_line_repetido_serial = self.env['stock.move.line'].search([('picking_id','=',self.stock_picking_id.id),('move_id','=',elem_move_picking.id),('product_id','=',elem_move_picking.product_id.id),('lot_name','=',str(elem[1]))])
									if len(move_line_repetido_serial)>0:
										if not ("Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])) in error_new:
											error_new = error_new + "Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])+"\n"
									elem_move_picking.sudo().price_unit_it = float(elem[4])
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_name':str(elem[1])
									}
									self.env['stock.move.line'].create(move_line_vals)


							elif self.env['product.product'].browse(mat[0]).tracking == 'none':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)==1:
									if not (elem_move_picking.id) in stock_moves_ya_limpios:
										for eliminar_moves in elem_move_picking.move_line_ids:
											eliminar_moves.sudo().unlink()
										stock_moves_ya_limpios.append(elem_move_picking.id)
									elem_move_picking.sudo().price_unit_it = float(elem[4])
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_name':str(elem[1])
									}
									self.env['stock.move.line'].create(move_line_vals)
					self.stock_picking_id.refresh()
					self.stock_picking_id.move_line_ids_without_package.refresh()
					if error_new != '':
						raise UserError(str(error_new))
					revision_final = ""
					for moves in self.stock_picking_id.move_ids_without_package:
						if moves.quantity_done > moves.product_uom_qty:
							if not ("Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)) in revision_final:
								revision_final = revision_final + "Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)+"\n"
					if revision_final!="":
						raise UserError(str(revision_final))
				else:
					data = base64.b64decode(self.file).decode('utf-8')
					info = data.split('\n')
					cont = 0
					verificacion_lotes = []
					contenedor_lotes = {}
					errores = ""
					for i in info:
						data_linea = i.split(';')
						if len(data_linea)==5:
							verificacion_lotes.append(data_linea[1].strip())                    

							producto = self.env['product.product'].search([(l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
							if len(producto)>0:
								existe_lote = self.env['stock.production.lot'].search([('name','=',data_linea[1].strip()),('product_id.'+l.stock_picking_id.tipo_import_lot,'=',data_linea[0].strip())])
								if len(existe_lote)==0 or len(existe_lote)>1 :
									if data_linea[1].strip() != "":
										errores += "No existe el lote para el producto seleccionado: (" + data_linea[0].strip()+ "," + data_linea[1].strip() + ")\n"
								key_imp = None
								if producto[0].tracking == 'lot':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,existe_lote.id)
								if producto[0].tracking == 'serial':
									if data_linea[1].strip()=='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", Trabaja Con Lotes/Series y No Se Ingreso Su Serial: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,existe_lote.id)
								if producto[0].tracking == 'none':
									if data_linea[1].strip()!='':
										if not ("Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) ) in errores:
											errores += "Producto Ingresado: " + data_linea[0].strip()+", No Trabaja Con Lotes/Series, Lote Ingresado: "+str(data_linea[1].strip()) + "\n"
									key_imp= (producto[0].id,data_linea[1].strip())
								if key_imp in contenedor_lotes:
									detalle_lotes = contenedor_lotes[key_imp]
									detalle_lotes.append(data_linea)
									contenedor_lotes[key_imp] = detalle_lotes
								else:
									contenedor_lotes[key_imp] = [data_linea]
							else:
								if ("No existe el producto: " + data_linea[0].strip() + "\n" ) in errores:
									pass
								else:
									errores += "No existe el producto: " + data_linea[0].strip()  + "\n"
						else:
							if len(data_linea)!=1:
								if not ("Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea)) in errores:
									errores += "Linea Ingresada No Respeta El Formato De 5 Campos: "+str(data_linea) + "\n"
					self.errores_txt = errores

					if errores != "":
						raise UserError(str(errores))
					lines_updated=[]
					error_new = ""
					for mat in contenedor_lotes:
						#C310|0E0VHV|67|01/18/2020|78.76|
						for elem in contenedor_lotes[mat]:
							lote = False
							existelote = False
							if mat[1]!=False:
								existelote = self.env['stock.production.lot'].search([('id','=',mat[1])])
								if len(existelote)==0 or len(existelote)>1:
									error_new += "No existe el lote para el producto seleccionado: (" + elem[0].strip()+ "," + elem[1].strip() + ")\n"
								else:
									lote = existelote.id
							if self.env['product.product'].browse(mat[0]).tracking == 'lot':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)!=0:
									if len(elem_move_picking)>1:
										raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
									if len(elem_move_picking)!=0:
										if len(elem_move_picking)==1:
											if not (elem_move_picking.id) in stock_moves_ya_limpios:
												for eliminar_moves in elem_move_picking.move_line_ids:
													eliminar_moves.sudo().unlink()
												stock_moves_ya_limpios.append(elem_move_picking.id)
											move_line_vals = {
												'picking_id': self.stock_picking_id.id,
												'location_dest_id': self.stock_picking_id.location_dest_id.id,
												'location_id': self.stock_picking_id.location_id.id,
												'product_id': elem_move_picking.product_id.id,
												'product_uom_id': elem_move_picking.product_uom.id,
												'qty_done': float(elem[2]),
												'package_level_id':False,
												'move_id':elem_move_picking.id,
												'lot_id':lote
											}
											self.env['stock.move.line'].create(move_line_vals)

							elif self.env['product.product'].browse(mat[0]).tracking == 'serial':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if elem[2] != "1":
									if not ("Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])) in error_new:
										error_new = error_new + "Ingreso Cantidades Incorrectas En Producto Con Seriales: "+str(self.env['product.product'].browse(mat[0]).name)+", serie:"+str(mat[1])+"\n"
								if len(elem_move_picking)==1:
									if not (elem_move_picking.id) in stock_moves_ya_limpios:
										for eliminar_moves in elem_move_picking.move_line_ids:
											eliminar_moves.sudo().unlink()
										stock_moves_ya_limpios.append(elem_move_picking.id)
									move_line_repetido_serial = self.env['stock.move.line'].search([('picking_id','=',self.stock_picking_id.id),('move_id','=',elem_move_picking.id),('product_id','=',elem_move_picking.product_id.id),('lot_id','=',lote)])
									if len(move_line_repetido_serial)>0:
										if not ("Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])) in error_new:
											error_new = error_new + "Ingreso Dos Movimientos del producto: "+str(elem_move_picking.product_id.name)+", Con El Mismo Nº Serial Unico:"+str(elem[1])+"\n"
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_id':lote
									}
									self.env['stock.move.line'].create(move_line_vals)


							elif self.env['product.product'].browse(mat[0]).tracking == 'none':
								elem_move_picking = self.env['stock.move'].search([('picking_id','=',self.stock_picking_id.id),('product_id','=',mat[0])])
								if len(elem_move_picking)>1:
									raise UserError("dos stockmoves:" +str(elem_move_picking[0].product_id.name))
								if len(elem_move_picking)==0:
									if not ("No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)) in error_new:
										error_new = error_new + "No Existe La Operación Con El Producto: "+str(self.env['product.product'].browse(mat[0]).name)+"\n"
								if len(elem_move_picking)==1:
									if not (elem_move_picking.id) in stock_moves_ya_limpios:
										for eliminar_moves in elem_move_picking.move_line_ids:
											eliminar_moves.sudo().unlink()
										stock_moves_ya_limpios.append(elem_move_picking.id)
									move_line_vals = {
										'picking_id': self.stock_picking_id.id,
										'location_dest_id': self.stock_picking_id.location_dest_id.id,
										'location_id': self.stock_picking_id.location_id.id,
										'product_id': elem_move_picking.product_id.id,
										'product_uom_id': elem_move_picking.product_uom.id,
										'qty_done': float(elem[2]),
										'package_level_id':False,
										'move_id':elem_move_picking.id,
										'lot_id':lote
									}
									self.env['stock.move.line'].create(move_line_vals)
					if error_new!="":
						raise UserError(str(error_new))
					revision_final = ""
					for moves in self.stock_picking_id.move_ids_without_package:
						if moves.quantity_done > moves.product_uom_qty:
							if not ("Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)) in revision_final:
								revision_final = revision_final + "Importación Erronea, Las Cantidades Ingresadas Superan A Las Demandadas: "+str(moves.name)+"\n"
					if revision_final!="":
						raise UserError(str(revision_final))
