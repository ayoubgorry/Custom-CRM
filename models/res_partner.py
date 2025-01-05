from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Selection([
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('distributor', 'Distributor')
    ], string='Type de Client')
    
    purchase_count = fields.Integer(string='Nombre d\'achats', compute='_compute_purchase_count', store=True)
    customer_rating = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ], string='Note Client', compute='_compute_customer_rating', store=True)

    @api.depends('sale_order_ids')
    def _compute_purchase_count(self):
        for partner in self:
            partner.purchase_count = len(partner.sale_order_ids.filtered(lambda s: s.state == 'sale'))

    @api.depends('purchase_count')
    def _compute_customer_rating(self):
        for partner in self:
            if partner.purchase_count == 0:
                partner.customer_rating = '1'
            elif partner.purchase_count <= 2:
                partner.customer_rating = '2'
            elif partner.purchase_count <= 5:
                partner.customer_rating = '3'
            elif partner.purchase_count <= 10:
                partner.customer_rating = '4'
            else:
                partner.customer_rating = '5'
