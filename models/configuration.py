from odoo import models, fields, api


class Vendors(models.Model):
    _name = 'vendors'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    id_num = fields.Char(string="ID Number")
    phone_num = fields.Char(string="Phone Number")
    active = fields.Boolean(string="Active", default=True)
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'This code is used before!'),
    ]


class Customers(models.Model):
    _name = 'customers'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    address = fields.Char(string="Address")
    phone_num = fields.Char(string="Phone Number")
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'This code is used before!'),
    ]


class Products(models.Model):
    _name = 'products'

    # product_id = fields.Many2one('daily.transport', string='Transport Products',
    #                              ondelete='cascade', index=True)

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'This code is used before!'),
    ]
