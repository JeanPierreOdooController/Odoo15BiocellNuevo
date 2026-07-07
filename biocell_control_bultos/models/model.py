from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError


class stock_quant_package_list_items(models.Model):
    _name = 'stock.quant.package.list.items'

    product_id = fields.Many2one('product.product','Producto',required=True)
    cantidad = fields.Float('Cantidad',required=True)
    package_list_id = fields.Many2one('stock.quant.package.list')

class stock_quant_package_list(models.Model):
    _name = 'stock.quant.package.list'

    name = fields.Char('Nombre Lista',required=True)
    items_ids = fields.One2many('stock.quant.package.list.items','package_list_id','Detalle')

class stock_quant_package(models.Model):
    _inherit='stock.quant.package'

    template_package_list_id = fields.Many2one('stock.quant.package.list','Plantilla Lista Empaque',required=True)
    status_validate = fields.Selection([('completo','Completo'),('incompleto','Incompleto')],'Contenido del Pack',compute="get_status_validate")
    status_manual = fields.Selection([('create','En Proceso de Creación'),('open','Libre para Uso'),('inspection','En Inspección')],'Ubicación',default='create')

    @api.depends('quant_ids.quantity','quant_ids','template_package_list_id.items_ids','template_package_list_id')
    def get_status_validate(self):
        for i in self:
            flag = 'completo'
            for elem in i.template_package_list_id.items_ids:
                lineas_rev = i.quant_ids.filtered(lambda r:r.product_id.id == elem.product_id.id)
                total_r = 0
                for xx in lineas_rev:
                    total_r += xx.quantity
                if total_r >= elem.cantidad:
                    pass
                else:
                    flag = 'incompleto'
            i.status_validate = flag


class product_template(models.Model):
    _inherit='product.template'

    no_accounting = fields.Boolean('Sin impacto contable',default=False)


class stock_package_reposition_items_lotes(models.Model):
    _name = 'stock.package.reposition.items.lotes'

    reposition_items_id = fields.Many2one('stock.package.reposition.items','Reposicion Linea')
    product_id = fields.Many2one('product.product','Producto',related='reposition_items_id.product_id')
    stock_lot_id = fields.Many2one('stock.quant','Lote/Serie')
    cantidad = fields.Float('Cantidad')

class stock_package_reposition_items(models.Model):
    _name = 'stock.package.reposition.items'

    package_reposition_id = fields.Many2one('stock.package.reposition','Reposición')
    product_id = fields.Many2one('product.product','Producto')
    cantidad = fields.Float('Cantidad')
    lotes = fields.One2many('stock.package.reposition.items.lotes','reposition_items_id','Lotes/Series')
    cantidad_x_procesar = fields.Float('Cantidad a Procesar',compute="get_cantidad_x_procesar")

    def get_cantidad_x_procesar(self):
        for i in self:
            cant = 0
            for l in i.lotes:
                cant += i.cantidad
            i.cantidad_x_procesar = cant


class stock_package_reposition(models.Model):
    _name = 'stock.package.reposition'

    package_id = fields.Many2one('stock.quant.package','Paquete',required=True,domain=[('status_validate','=','incompleto')])
    details = fields.One2many('stock.package.reposition.items','package_reposition_id','Faltante')
    picking_ids = fields.One2many('stock.picking','reposition_id','Albaranes')
    state = fields.Selection([('draft','Borrador'),('search','Por Completar'),('done','Terminado')],'Estado',default='draft')

    def volverborrador(self):
        self.state = 'draft'

    def completar(self):
        for i in self:
            if i.package_id.id:
                for x in i.package_id.template_package_list_id.items_ids:
                    lineas_revision = i.package_id.quant_ids.filtered(lambda r:r.product_id.id == x.product_id.id)
                    total_r = 0
                    for gg in lineas_revision:
                        total_r += gg.quantity
                    if total_r < x.cantidad:
                        linea = self.env['stock.package.reposition.items'].create({
                            'package_reposition_id':i.id,
                            'product_id':x.product_id.id,
                            'cantidad':x.cantidad - total_r,
                            })
            i.state = 'search'

    def validar(self):
        for i in self:
            type_op = self.env['stock.picking.type'].sudo().search([('name','=','Reposición Transferencias'),('company_id','=',self.env.company.id)])
            if len(type_op)>0:
                type_op = type_op[0]
            else:
                type_op = self.env['stock.picking.type'].sudo().create({
                    'name':"Reposición Transferencias",
                    'code':'internal',
                    'company_id':self.env.company.id,
                    'show_operations':True,
                    'sequence_code':'reptransf',
                    'use_existing_lots':True,
                    'default_location_src_id': self.env['stock.location'].sudo().search([('company_id','=',self.env.company.id),('usage','=','internal')])[0].id,
                    'default_location_dest_id': self.env['stock.location'].sudo().search([('company_id','=',self.env.company.id),('usage','=','internal')])[0].id,
                    })

            self.env.cr.execute("""

                select distinct sq.location_id 
                from stock_package_reposition_items spri
                inner join stock_package_reposition_items_lotes spril on spril.reposition_items_id = spri.id
                inner join stock_quant sq on sq.id = spril.stock_lot_id
                where spri.package_reposition_id = """+str(i.id)+"""
                """)
            for picking in self.env.cr.fetchall():
                self.env['stock.picking'].sudo().create({
                    'partner_id':self.env.user.partner_id.id,
                    'type_operation_sunat_id':self.env['type.operation.kardex'].sudo().search([('code','=','11')])[0].id,
                    'picking_type_id':type_op.id,
                    'location_id':picking[0],
                    'location_dest_id':i.package_id.location_id.id,
                    'reposition_id':i.id,
                    'state':'assigned',
                    })

            i.refresh()
            for gg in i.details:
                for ga in gg.lotes:
                    movet = self.env['stock.move'].sudo().create({
                        'product_id':ga.stock_lot_id.product_id.id,
                        'product_uom_qty': ga.cantidad,
                        'name': ga.stock_lot_id.product_id.name_get()[0][1],
                        'product_uom': ga.stock_lot_id.product_id.uom_id.id,
                        'location_id':ga.stock_lot_id.location_id.id,
                        'location_dest_id':i.package_id.location_id.id,
                        'picking_type_id':type_op.id,
                        'price_unit_it': 0,
                        'picking_id': i.picking_ids.filtered(lambda r:r.location_id.id == ga.stock_lot_id.location_id.id)[0].id,
                        'state':'assigned',
                    })

                    if i.package_id.location_id.id == 39:
                        raise UserError("Las reposiciones solo se manejan en Lima Paquetes.")

                    self.env['stock.move.line'].sudo().create({
                        'product_id':ga.stock_lot_id.product_id.id,
                        'product_uom_qty': ga.cantidad,
                        'qty_done': ga.cantidad,
                        'product_uom_id': ga.stock_lot_id.product_id.uom_id.id,
                        'location_id':ga.stock_lot_id.location_id.id,
                        'location_dest_id':i.package_id.location_id.id,
                        'picking_id': movet.picking_id.id,
                        'lot_id':ga.stock_lot_id.lot_id.id,
                        'move_id':movet.id,
                        'state':'assigned',
                        'package_id':ga.stock_lot_id.package_id.id,
                        'result_package_id':i.package_id.id,
                    })

                    self.env.cr.execute(""" 
                        update stock_quant set reserved_quantity = reserved_quantity+ """+str(ga.cantidad)+"""
                        where id = """ +str(ga.stock_lot_id.id)+"""
                     """)
                    ga.stock_lot_id.refresh()

            for pic in i.picking_ids:
                rpta = pic.button_validate()
                if rpta and str(type(rpta)) !="<class 'bool'>" and  rpta['res_model'] == 'expiry.picking.confirmation':
                    confirm = self.env['expiry.picking.confirmation'].sudo().create({
                        'lot_ids':rpta['context']['default_lot_ids'],
                        'picking_ids':rpta['context']['default_picking_ids'],
                        })
                    confirm.with_context(button_validate_picking_ids=rpta['context']['button_validate_picking_ids'],default_lot_ids=rpta['context']['default_lot_ids']).process()

            i.state = 'done'

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    reposition_id = fields.Many2one('stock.package.reposition','Reposición')
    package_id = fields.Many2one('stock.quant.package','Paquete')

    def update_package_id(self):
        for i in self:
            if i.package_id.id:
                for l in i.package_id.quant_ids:
                    movet = self.env['stock.move'].sudo().create({
                        'product_id':l.product_id.id,
                        'product_uom_qty': l.quantity,
                        'name': l.product_id.name_get()[0][1],
                        'product_uom': l.product_id.uom_id.id,
                        'location_id':l.location_id.id,
                        'location_dest_id':i.location_dest_id.id,
                        'picking_type_id':i.picking_type_id.id,
                        'price_unit_it': 0,
                        'picking_id': i.id,
                        'state':'assigned',
                    })

                    self.env['stock.move.line'].sudo().create({
                        'product_id':l.product_id.id,
                        'product_uom_qty': l.quantity,
                        'qty_done': l.quantity,
                        'product_uom_id': l.product_id.uom_id.id,
                        'location_id': movet.location_id.id,
                        'location_dest_id':movet.location_dest_id.id,
                        'picking_id': i.id,
                        'lot_id':l.lot_id.id,
                        'move_id':movet.id,
                        'state':'assigned',
                        'package_id':i.package_id.id,
                        'result_package_id':i.package_id.id,
                    })

                    self.env.cr.execute("""
                        update stock_quant set reserved_quantity = reserved_quantity+ """+str(l.quantity)+"""
                        where id = """ +str(l.id)+"""
                     """)
                    
                    self.env.cr.execute("""
                         select reserved_quantity,quantity from stock_quant where id = """+str(l.id)+"""
                    """)
                    data = self.env.cr.fetchall()[0]
                    if data[0]>data[1]:
                        raise UserError("No se puede reservar porque no dispone de dicha cantidad: " + str(l.product_id.name_get()[0][1] ))
                    l.refresh()

    def sale_package_id(self):
        for i in self:
            flag = False
            for op in i.move_ids_without_package:
                if op.sale_line_id.id:
                    flag = True

            if flag:
                i.do_unreserve()
                for op in i.move_ids_without_package:
                    if op.sale_line_id.id:                        
                        if op.sale_line_id.quant_id.id:
                            xax = op.sale_line_id.quant_id
                            self.env['stock.move.line'].sudo().create({
                                'product_id':xax.product_id.id,
                                'product_uom_qty': xax.quantity,
                                'qty_done': xax.quantity,
                                'product_uom_id': xax.product_id.uom_id.id,
                                'location_id': op.location_id.id,
                                'location_dest_id':op.location_dest_id.id,
                                'picking_id': i.id,
                                'lot_id':xax.lot_id.id,
                                'move_id':op.id,
                                'state':'assigned',
                                'package_id':op.sale_line_id.package_id.id,
                                'result_package_id':op.sale_line_id.package_id.id,
                            })                                    
                            self.env.cr.execute("""
                                update stock_quant set reserved_quantity = reserved_quantity+ """+str(xax.quantity)+"""
                                where id = """ +str(xax.id)+"""
                             """)
                            self.env.cr.execute("""
                                select reserved_quantity,quantity from stock_quant where id = """+str(xax.id)+"""
                            """)
                            data = self.env.cr.fetchall()[0]
                            if data[0]>data[1]:
                                raise UserError("No se puede reservar porque no dispone de dicha cantidad: " + str(xax.product_id.name_get()[0][1] ))
                            op.refresh()
                            op.state = 'assigned'           
                        else:
                            op._action_assign()



class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    package_id = fields.Many2one('stock.quant.package','Paquete')
    quant_id = fields.Many2one('stock.quant','Paquete')

class sale_order(models.Model):
    _inherit = 'sale.order'

    package_id = fields.Many2one('stock.quant.package','Paquete')

    """
    def action_confirm(self):
        t = super(sale_order,self).action_confirm()
        for i in self:
            for l in i.picking_ids:
                if l.state not in ('done','cancel'):
                    l.sale_package_id()
        return t
    """

    def update_package_id(self):
        for i in self:
            if i.package_id.id:
                self.env['sale.order.line'].sudo().create({
                    'order_id':i.id,
                    'display_type':'line_section',
                    'name':'Inicio de Paquete: ' + i.package_id.name,
                    'sale_type':'sale',
                    })

                for l in i.package_id.quant_ids:
                    self.env['sale.order.line'].sudo().create({
                        'order_id':i.id,
                        'product_id':l.product_id.id,
                        'name':l.product_id.name_get()[0][1] + 'Paquete: ' + i.package_id.name + ' - Lote/Serie: ' + (l.lot_id.name or 'S/N'),
                        'product_uom_qty':l.quantity,
                        'product_uom':l.product_id.uom_id.id,
                        'tax_id':l.product_id.taxes_id.filtered(lambda r: r.company_id.id == self.env.company.id).ids,
                        'package_id':i.package_id.id,
                        'quant_id':l.id,
                    'sale_type':'sale',
                        })

                self.env['sale.order.line'].sudo().create({
                    'order_id':i.id,
                    'display_type':'line_section',
                    'name':'Fin de Paquete: ' + i.package_id.name,
                    'sale_type':'sale',
                    })
