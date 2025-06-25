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
            for move_line in self.move_line_ids:
                move_line.result_package_id = None
