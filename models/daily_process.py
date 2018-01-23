from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Daily_transport(models.Model):
    _name = 'daily.transport'
    _rec_name = 'date'

    @api.one
    @api.depends('daily_transport_line')
    def _compute_total_quantities(self):
        self.trans_total_quantities = sum(line.trans_quantity for line in self.daily_transport_line)
        self.trans_total_remaining = sum(line.trans_remaining for line in self.daily_transport_line)
        if self.trans_total_quantities == self.trans_total_remaining:
            self.state = 'new'
        elif self.trans_total_remaining != self.trans_total_quantities and self.trans_total_remaining != 0:
            self.state = 'processing'
        elif self.trans_total_remaining == 0:
            self.state = 'done'

    # @api.multi
    # @api.onchange('daily_transport_line.trans_product_id')
    # @api.depends('daily_transport_line.trans_product_id')
    # def _get_trans_products(self):
    #     for l in self.daily_transport_line:
    #         self.daily_trans_product_id = l.trans_product_id.id
    #         print self.daily_trans_product_id

    name = fields.Char(string="Name")
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    vendor_id = fields.Many2one('vendors', string='Vendor', required=True)
    state = fields.Selection(
            [('new', 'New'), ('processing', 'Processing'), ('done', 'Done'), ],
            string='Status', compute='_compute_total_quantities')

    daily_transport_line = fields.One2many('daily.transport.line', 'info_id', string='Transport Info',
                                           copy=True)

    selling_line = fields.One2many('selling.line', 'sell_id', string='Selling Info',
                                   copy=True)

    trans_total_quantities = fields.Float(string="Total Transport Quantity", compute='_compute_total_quantities')
    trans_total_remaining = fields.Float(string="Total Remaining Quantity", compute='_compute_total_quantities')

    # daily_trans_product_ids = fields.One2many('products', 'product_id', string='Products',
    #                                           compute='_get_trans_products')

    cp_nmb_lines = fields.Integer(string="Number Of Lines")
    cp_product_id = fields.Many2one('products', string='Products')
    cp_container = fields.Selection(
            [('kafs', 'Kafs'), ('barnika', 'Barnika'), ('other', 'Other')],
            string='Container')

    @api.multi
    def button_create_entries(self):
        # print self.env.user.company_id.bia3a_value
        if self.cp_nmb_lines <= 0:
            pass
        else:
            for i in range(self.cp_nmb_lines):
                self.selling_line.create({
                    'sell_id': self.id,
                    'sell_product_id': self.cp_product_id.id,
                    'sell_container': self.cp_container,
                })


class Daily_transport_info(models.Model):
    _name = 'daily.transport.line'

    @api.multi
    @api.onchange('trans_quantity')
    def _compute_remaining_quantity(self):
        for l in self:
            trans_prod = l.trans_product_id.id
            child_categs = self.env['selling.line'].search(
                    [('sell_product_id', '=', trans_prod), ('sell_id', '=', l.info_id.id)])
            if child_categs:
                l.trans_remaining = l.trans_quantity - sum(line.sell_quantity for line in child_categs)
                l.trans_weight = sum(line.sell_weight for line in child_categs)
                if l.trans_remaining < 0:
                    raise ValidationError(_('ERROR'))
            else:
                l.trans_remaining = l.trans_quantity

    info_id = fields.Many2one('daily.transport', string='Transport Reference',
                              ondelete='cascade', index=True)
    trans_product_id = fields.Many2one('products', string='Products', required=True)
    trans_quantity = fields.Integer(string="Quantity")
    trans_container = fields.Selection(
            [('kafs', 'Kafs'), ('barnika', 'Barnika'), ('other', 'Other')],
            string='Container')
    trans_weight = fields.Float(string="Weight", compute='_compute_remaining_quantity')
    trans_remaining = fields.Integer(string="Remaining", compute='_compute_remaining_quantity')


class Selling_info(models.Model):
    _name = 'selling.line'

    @api.multi
    @api.onchange('sell_weight', 'sell_unit_price')
    def _compute_sell_line_total(self):
        bia3a = self.env.user.company_id.bia3a_value
        for l in self:
            l.sell_line_total = l.sell_weight * l.sell_unit_price
            l.sell_line_full_total = (l.sell_weight * l.sell_unit_price) + (bia3a * l.sell_quantity)

    # @api.onchange('sell_product_id')
    # def _products_domain(self):
    #     domain = []
    #     for l in self:
    #         parent_categs = self.env['daily.transport.line'].search([('info_id', '=', l.sell_id.id)])
    #         if parent_categs:
    #             for ll in parent_categs:
    #                 domain.append(ll.trans_product_id.id)
    #     print domain
    #     return domain

    # , domain=_products_domain
    sell_id = fields.Many2one('daily.transport', string='Selling Reference',
                              ondelete='cascade', index=True)
    vendor_id = fields.Many2one('vendors', related='sell_id.vendor_id', string="Vendor", store=True)
    date = fields.Date(related='sell_id.date', string="Date", store=True)
    sell_customer_id = fields.Many2one('customers', string='Customers')
    sell_product_id = fields.Many2one('products', string='Products', required=True)
    sell_quantity = fields.Integer(string="Quantity")
    sell_container = fields.Selection(
            [('kafs', 'Kafs'), ('barnika', 'Barnika'), ('other', 'Other')],
            string='Container')
    sell_weight = fields.Float(string="Weight")
    sell_unit_price = fields.Float(string="Unit Price")
    sell_line_total = fields.Float(string="Line Total", compute='_compute_sell_line_total')
    sell_line_full_total = fields.Float(string="Line Total with Bia3a", compute='_compute_sell_line_total')


class ResCompany(models.Model):
    _inherit = 'res.company'
    bia3a_value = fields.Float(string='Bia3a')
