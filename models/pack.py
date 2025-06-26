from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
import base64
from datetime import date,datetime

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    move_line_ids = fields.One2many(comodel_name='stock.move.line',inverse_name='result_package_id',string='Operaciones')

    def rya_unpack(self):
        self.ensure_one()
        if self.quant_ids:
            self.unpack()
        else:
            dict_products = {}
            for move_line in self.move_line_ids:
                qty = move_line.quantity
                if move_line.lot_id:
                    move_line.result_package_id = None
                elif not move_line.lot_id:
                    domain = [
                        ('picking_id','=',move_line.picking_id.id),
                        ('result_package_id','=',False),
                        ('id','!=',move_line.id),
                        ('product_id','=',move_line.product_id.id),
                        ('lot_id','=',None),
                        ]
                    other_move_line = self.env['stock.move.line'].search(domain,limit = 1)
                    if other_move_line:
                        other_move_line.quantity = other_move_line.quantity + move_line.quantity
                        move_line.unlink()
                    else:
                        move_line.result_package_id = None
