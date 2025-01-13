from odoo import models, fields, api

class Contact(models.Model):
    _name = 'site.contact'
    _description = 'Site Contact'
    _rec_name = 'name'

    icon = fields.Char(string='Icon', default='👤')
    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    status = fields.Selection([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red')
    ], string='Status', default='green')
    address = fields.Text(string='Address')
    rep_status = fields.Selection([
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ], string='Rep Status', default='Active')
    promo_ref = fields.Char(string='Promo Reference')
    frequency = fields.Integer(string='Frequency')
    rolling_frequency = fields.Char(string='Rolling Frequency')
    territory = fields.Char(string='Territory')
    notes = fields.Text(string='Notes')
    fax = fields.Char(string='Fax')
    latitude = fields.Float(string='Latitude', digits=(16, 6))
    longitude = fields.Float(string='Longitude', digits=(16, 6))
    site_id = fields.Many2one('site.site', string='Site', required=True, ondelete='cascade')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'Email must be unique!')
    ] 