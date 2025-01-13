from odoo import models, fields, api

class Site(models.Model):
    _name = 'site.site'
    _description = 'Site'
    _rec_name = 'name'

    icon = fields.Char(string='Icon', default='🏪')
    name = fields.Char(string='Name', required=True)
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    status = fields.Selection([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red')
    ], string='Status', default='green')
    active = fields.Boolean(default=True)
    contact_ids = fields.One2many('site.contact', 'site_id', string='Contacts')
    contact_count = fields.Integer(string='Contact Count', compute='_compute_contact_count')

    @api.depends('contact_ids')
    def _compute_contact_count(self):
        for record in self:
            record.contact_count = len(record.contact_ids)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Site code must be unique!')
    ] 