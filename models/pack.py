from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
import base64
from datetime import date,datetime

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    move_line_ids = fields.One2many(comodel_name='stock.move.line',inverse_name='result_package_id',string='Operaciones')
