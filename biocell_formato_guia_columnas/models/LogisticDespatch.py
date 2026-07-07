from odoo  import models,fields,api

class LogisticDespatch(models.Model):
    _inherit="logistic.despatch"
    
    def get_move_stock_by_product_report(self,product_id):
        if not self.picking_ids:
            return
        
        pick=self.env['stock.picking'].search([
            ('despatch_id','=',self.id)
        ],limit=1)
        
        moves=self.env['stock.move'].search([
            ('picking_id','=',pick.id),
            ('product_id','=',product_id.id)
        ])
        
        result=[]
        for move in moves.move_line_ids:
            stock_data={
                'lot':move.lot_id.name if move.lot_id else "",
                'expiration':move.lot_id.expiration_date if move.lot_id else "",
                'qty':move.qty_done,
            }
            result.append(stock_data)
        
        return result

    
