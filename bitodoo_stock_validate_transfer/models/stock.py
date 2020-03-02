# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import Warning


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if self.picking_type_id.code == "internal" or self.picking_type_id.code == "outgoing":
            location_origin_names = [x.location_id.display_name for x in self.move_lines if x.location_id.id != self.location_id.id]
            location_dest_names = [x.location_dest_id.display_name for x in self.move_lines if x.location_dest_id.id != self.location_dest_id.id]
            if location_origin_names:
                msm = u"las ubicaciones de origén [{}] son diferentes a la ubicación de la transferencia ({})"
                raise Warning(msm.format(', '.join(location_origin_names), self.location_id.name))
            if location_dest_names:
                msm = u"las ubicaciones de destino [{}] son diferentes a la ubicación de la transferencia ({})"
                raise Warning(msm.format(', '.join(location_dest_names), self.location_dest_id.name))

            for line in self.move_line_ids:
                product_name = line.product_id.display_name
                if not line.product_id.type == 'product':
                    raise Warning(u"El producto {} debe ser de tipo Almacenable.".format(product_name))
                if self.location_id.id:
                    obj_sq = self.env['stock.quant'].search([
                                                            ('location_id', '=', self.location_id.id),
                                                            ('product_id', '=', line.product_id.id)
                                                            ])
                    product_stock_qty = sum([x.quantity for x in obj_sq if x.quantity])
                    product_qty = line.qty_done
                    name_warehouse = str(self.location_id.name) + " - " + str(self.location_id.location_id.name)
                    if product_qty > product_stock_qty:
                        if product_qty <= 0:
                            msm = "No puede transferir el producto {} con cantidad menor o igual a 0"
                            raise Warning(msm.format(line.product_id.name))
                        else:
                            msm = u"Usted planea transferir {} {} pero solo tiene {} en {}"
                            messaje = msm.format(product_qty, product_name, product_stock_qty, name_warehouse)
                            raise Warning(messaje)

        res = super(StockPicking, self).button_validate()
        return res
