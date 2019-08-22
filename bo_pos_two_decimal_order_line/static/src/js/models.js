odoo.define('bo_pos_two_decimal_order_line.models', function (require) {
"use strict";

    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');

    // Ref. inherit pos-addons/pos_product_available/static/src/js/pos.js
    var PosModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        load_server_data: function(){
            var self = this;

            var loaded = PosModelSuper.load_server_data.call(this);
            var currency_model = _.find(this.models, function(model){
                return model.model === 'res.currency';
            });
            if (currency_model) {
                var loaded_super = currency_model.loaded;
                currency_model.loaded = function(that, currencies){
                    loaded_super(self, currencies);
                    self.currency = currencies[0];
                    if (self.currency.rounding > 0 && self.currency.rounding < 1) {
                        self.currency.decimals = 2;
                        self.currency.rounding = 0.1;
                    } else {
                        self.currency.decimals = 0;
                    }
                };
            }
            return loaded;
        },
    });
});