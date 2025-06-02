from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
import base64
from datetime import date,datetime

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def btn_add_packages(self):
        self.ensure_one()
        vals = {
                'picking_id': self.id,
                }
        wizard_id = self.env['add.packages.wizard'].create(vals)
        domain = [('picking_id','=',self.id),('result_package_id','=',False)]
        move_lines = self.env['stock.move.line'].search(domain)
        if not move_lines:
            raise ValidationError('No hay operaciones sin paquete asignado')
        for move_line in move_lines:
            vals_line = {
                    'wizard_id': wizard_id.id,
                    'move_line_id': move_line.id,
                    'original_quantity': move_line.quantity,
                    'final_quantity': move_line.quantity,
                    }
            line_id = self.env['add.packages.line.wizard'].create(vals_line)
        return {
                'name': _('Add Packages'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'add.packages.wizard',
                'res_id': wizard_id.id,
                'target': 'new',
                'type': 'ir.actions.act_window',
            }
