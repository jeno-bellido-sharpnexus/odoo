from odoo import models, fields, api

class SampleRecord(models.Model):
    _name = 'sample.record'
    _description = 'Sample Record'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string='Status', default='draft', required=True)
    amount = fields.Float(string='Amount', digits=(10, 2))
    is_active = fields.Boolean(string='Active', default=True)
    
    # Relationship fields
    partner_id = fields.Many2one('res.partner', string='Related Partner')
    
    @api.model
    def create(self, vals):
        return super(SampleRecord, self).create(vals)
    
    def write(self, vals):
        return super(SampleRecord, self).write(vals)
    
    def unlink(self):
        return super(SampleRecord, self).unlink()
    
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
    
    def action_done(self):
        for record in self:
            record.state = 'done'
    
    def action_reset(self):
        for record in self:
            record.state = 'draft' 