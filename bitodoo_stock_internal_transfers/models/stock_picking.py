# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import Warning



class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def state_list(self):
        for line in self.move_lines:
            product_name = line.product_id.display_name
            if not line.product_id.type == 'product':
                raise Warning(u"El producto {} debe ser de tipo Almacenable.".format(product_name))
            if self.location_id.id:
                product_stock_qty = line.product_id.with_context({'location': self.location_id.id}).qty_available
                product_qty = line.quantity_done
                name_warehouse = self.location_id.name
                if product_qty > product_stock_qty and self.picking_type_id.code != 'incoming':
                    messaje = u"Usted planea transferir {} {} pero solo tiene {} en {} ".format(product_qty, product_name, product_stock_qty, name_warehouse)
                    raise Warning(messaje)

        for line in self.move_line_ids:
            product_name = line.product_id.display_name
            if not line.product_id.type == 'product':
                raise Warning(u"El producto {} debe ser de tipo Almacenable.".format(product_name))
            if self.location_id.id:
                product_stock_qty = line.product_id.with_context({'location': self.location_id.id}).qty_available
                product_qty = line.qty_done
                name_warehouse = self.location_id.name
                if product_qty > product_stock_qty and self.picking_type_id.code != 'incoming':
                    messaje = u"Usted planea transferir {} {} pero solo tiene {} en {} ".format(product_qty, product_name, product_stock_qty, name_warehouse)
                    raise Warning(messaje)
        
        for rec in self:
            rec.state = 'assigned'
    

    @api.one
    def action_cancel(self):
        r = super(StockPicking, self).action_cancel()
        if self.condition_delivery:
            self.state = "cancel"
        return r

    @api.multi
    def button_validate(self):
        if self.picking_type_id.code == "internal":
            for line in self.move_lines:
                product_name = line.product_id.display_name
                if not line.product_id.type == 'product':
                    raise Warning(u"El producto {} debe ser de tipo Almacenable.".format(product_name))
                if self.location_id.id:
                    product_stock_qty = line.product_id.with_context({'location': self.location_id.id}).qty_available
                    product_qty = line.quantity_done
                    name_warehouse = self.location_id.name
                    if product_qty > product_stock_qty:
                        messaje = u"111Usted planea transferir {} {} pero solo tiene {} en {} ".format(product_qty, product_name, product_stock_qty, name_warehouse)
                        raise Warning(messaje)

            for line in self.move_line_ids:
                product_name = line.product_id.display_name
                if not line.product_id.type == 'product':
                    raise Warning(u"El producto {} debe ser de tipo Almacenable.".format(product_name))
                if self.location_id.id:
                    product_stock_qty = line.product_id.with_context({'location': self.location_id.id}).qty_available
                    product_qty = line.qty_done
                    name_warehouse = self.location_id.name
                    if product_qty > product_stock_qty and self.picking_type_id.code != 'incoming':
                        messaje = u"Usted planea transferir {} {} pero solo tiene {} en {} ".format(product_qty, product_name, product_stock_qty, name_warehouse)
                        raise Warning(messaje)

        return super(StockPicking, self).button_validate()
