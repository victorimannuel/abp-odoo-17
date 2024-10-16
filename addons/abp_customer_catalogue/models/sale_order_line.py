import json
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    product_template_domain = fields.Json(compute='_compute_product_template_domain')
    
    # customer_catalogue_id = fields.Many2one(comodel_name='customer.catalogue', compute='_compute_customer_catalogue')
    customer_catalogue_id = fields.Many2one(comodel_name='customer.catalogue')
    customer_catalogue_domain = fields.Json(compute='_compute_customer_catalogue_domain')
    customer_product_code = fields.Char(string='Customer Product Code')
    customer_product_ref = fields.Char(string='Customer Product Ref')
    
    @api.depends('order_id.partner_id', 'order_id.show_all_product')
    def _compute_product_template_domain(self):
        for rec in self:
            product_template = rec.env['product.template'].search([
                ('customer_catalogue_ids.partner_id', '=', rec.order_id.partner_id.id),
            ])
            if rec.order_id.show_all_product:
                rec.product_template_domain = json.dumps([('sale_ok', '=', True)])
            else:
                rec.product_template_domain = json.dumps([('id', 'in', product_template.ids), ('sale_ok', '=', True)])
            
    @api.depends('product_template_id', 'order_id.partner_id')
    def _compute_customer_catalogue_domain(self):
        for rec in self:
            customer_catalogue = rec.env['customer.catalogue'].search([
                ('partner_id', '=', rec.order_id.partner_id.id),
                ('product_tmpl_id', '=', rec.product_template_id.id),
            ])
            if customer_catalogue:
                rec.customer_catalogue_domain = json.dumps([('id', 'in', customer_catalogue.ids)])
            else:
                rec.customer_catalogue_domain = False
            if len(customer_catalogue.ids) == 1:
                rec.customer_catalogue_id = customer_catalogue
                rec.customer_product_code = customer_catalogue.customer_product_code
                rec.customer_product_ref = customer_catalogue.customer_product_ref
                rec.barcode = rec.pricelist_item_id.barcode
                rec.retail_price = rec.pricelist_item_id.retail_price
            
    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            rec.customer_catalogue_id = False
    
    @api.onchange('customer_catalogue_id')
    def _onchange_customer_catalogue_id(self):
        for rec in self:
            pricelist_item = False
            if rec.product_id:
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', rec.order_id.pricelist_id.id),
                    ('product_tmpl_id', '=', rec.product_template_id.id),
                    ('customer_product_ref', '=', rec.customer_catalogue_id.customer_product_ref),
                ])
                rec.barcode = pricelist_item.barcode
                rec.retail_price = pricelist_item.retail_price
                rec.price_unit = pricelist_item.distributor_price
                rec.pricelist_item_id = pricelist_item
                
            rec.customer_product_code = rec.customer_catalogue_id.customer_product_code
            rec.customer_product_ref = rec.customer_catalogue_id.customer_product_ref
                
    # @api.depends('product_template_id', 'order_id.partner_id')
    # def _compute_customer_catalogue(self):
    #     for rec in self:
    #         customer_catalogue = rec.env['customer.catalogue'].search([
    #             ('partner_id', '=', rec.order_id.partner_id.id),
    #             ('product_tmpl_id', '=', rec.product_template_id.id),
    #         ])
    #         rec.customer_catalogue_id = customer_catalogue
    #         if rec.customer_catalogue_id:
    #             rec.customer_product_code = rec.customer_catalogue_id.customer_product_code
    #             rec.customer_product_ref = rec.customer_catalogue_id.customer_product_ref
    