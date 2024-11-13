from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    customer_product_ref = fields.Char(string='Customer Product Ref', compute='_compute_pricelist_item_id')
    barcode = fields.Char(string='EAN13', compute='_compute_pricelist_item_id')
    retail_price = fields.Float(string="Retail Price", compute='_compute_pricelist_item_id')
    
    # Override parent method
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_pricelist_item_id(self):
        for rec in self:
            super()._compute_pricelist_item_id()
            rec.customer_product_ref = rec.barcode = False
            rec.retail_price = 0.0
            if rec.pricelist_item_id:
                rec.customer_product_ref = rec.pricelist_item_id.customer_product_ref
                rec.barcode = rec.pricelist_item_id.barcode
                rec.retail_price = rec.pricelist_item_id.retail_price or rec.pricelist_item_id.fixed_price
                