from odoo import models, fields, api

class SampleRecord(models.Model):
    _name = 'sample.record'
    _description = 'Sample Record'

    name = fields.Char(string='Name', required=True)
    icon = fields.Char(string='Icon')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    status = fields.Selection([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red')
    ], string='Status', default='green')
    address = fields.Char(string='Address')
    rep_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Rep Status', default='active')
    promo_ref = fields.Selection([
        ('live', 'Live'),
        ('draft', 'Draft')
    ], string='Promo Reference', default='draft')
    frequency = fields.Integer(string='Frequency')
    rolling_frequency = fields.Char(string='Rolling Frequency')
    territory = fields.Char(string='Territory')
    notes = fields.Text(string='Notes')
    fax = fields.Char(string='Fax')
    latitude = fields.Float(string='Latitude', digits=(16, 6))
    longitude = fields.Float(string='Longitude', digits=(16, 6))
    site_id = fields.Integer(string='Site ID')
    
    # Relationship fields
    partner_id = fields.Many2one('res.partner', string='Related Partner')
    
    @api.model
    def create(self, vals):
        return super(SampleRecord, self).create(vals)
    
    def write(self, vals):
        return super(SampleRecord, self).write(vals)
    
    def unlink(self):
        return super(SampleRecord, self).unlink() 