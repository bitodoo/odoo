# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import Warning


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        domain=[('usage', '=', 'internal')])
    location_dest_id = fields.Many2one(
        comodel_name='stock.location',
        domain=[('usage', '=', 'internal')])
    picking_type_id = fields.Many2one(
        comodel_name='stock.picking.type',
        domain=[('code', '=', 'internal')])

    def action_assign(self):
    	for line in self.move_lines:
            product_name = line.product_id.display_name
            if not line.product_id.type == 'product':
                raise Warning("El producto {} debe ser de tipo Almacenable.".format(product_name))
            if self.location_id.id:
                obj_sq = self.env['stock.quant'].search([('location_id', '=', self.location_id.id),('product_id', '=', line.product_id.id)])
                product_stock_qty = sum([x.qty for x in obj_sq if x.qty])
                product_qty = line.product_uom_qty
                name_warehouse = self.location_id.name
                if product_qty > product_stock_qty:
                    messaje = "Usted planea vender {} {} pero solo tiene {} en {} ".format(product_qty, product_name, product_stock_qty, name_warehouse)
                    raise Warning(messaje)
        res = super(StockPicking, self).action_assign()
        return res


