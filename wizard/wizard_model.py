# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _, Command
from odoo.exceptions import ValidationError
from odoo.tools import format_amount
from datetime import datetime

class AddPackagesWizard(models.TransientModel):
    _name = 'add.packages.wizard'
    _description = 'Add packages wizard'

    picking_id = fields.Many2one('stock.picking','Transferencia')
    package_name = fields.Char('Paquete')
    line_ids = fields.One2many(comodel_name='add.packages.line.wizard',inverse_name='wizard_id',string='Lineas')

    def btn_confirm(self):
        for line in self.line_ids:
            if line.final_quantity <= 0 or line.final_quantity > line.original_quantity:
                raise ValidationError('Cantidad incorrecta para producto %s'%(line.product_id.display_name))
        pack_name = self.package_name
        if not pack_name:
            raise ValidationError('Ingrese nombre del paquete')
        pack_id = self.env['stock.quant.package'].search([('name','=',pack_name)])
        if pack_id:
            raise ValidationError('Paquete existente')
        pack_id = self.env['stock.quant.package'].create({'name': pack_name})
        for line in self.line_ids:
            if line.original_quantity == line.final_quantity:
                move_line = line.move_line_id
                move_line.result_package_id = pack_id.id
            else:
                move_line = line.move_line_id
                original_quantity = line.original_quantity
                new_line = move_line.copy({'quantity': original_quantity - line.final_quantity})
                move_line.quantity = line.final_quantity
                move_line.result_package_id = pack_id.id

class AddPackagesLineWizard(models.TransientModel):
    _name = 'add.packages.line.wizard'
    _description = 'Add packages line wizard'

    wizard_id = fields.Many2one('add.packages.wizard',string='Wizard')
    move_line_id = fields.Many2one('stock.move.line','Operacion')
    product_id = fields.Many2one('product.product','Producto',related='move_line_id.product_id')
    original_quantity = fields.Float('Cantidad Original')
    final_quantity = fields.Float('Cantidad Final')

