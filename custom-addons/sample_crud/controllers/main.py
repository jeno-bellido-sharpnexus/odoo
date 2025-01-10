from odoo import http
from odoo.http import request, Response
import json

class SampleAPI(http.Controller):
    @http.route('/api/sample/records', auth='public', type='http', methods=['GET'], csrf=False)
    def get_records(self, **kwargs):
        try:
            # Access your custom model
            sample_records = request.env['sample.record'].sudo().search([])
            
            # Access built-in res.partner model (contacts)
            partners = request.env['res.partner'].sudo().search([], limit=5)
            
            # Access built-in sale.order model (if sale module is installed)
            sales = request.env['sale.order'].sudo().search([], limit=5) if 'sale.order' in request.env else []
            
            data = {
                'sample_records': [{
                    'id': record.id,
                    'name': record.name,
                    'description': record.description,
                    'date': str(record.date),
                    'state': record.state,
                    'amount': record.amount,
                    'is_active': record.is_active,
                    'partner_id': record.partner_id.id if record.partner_id else False,
                    'partner_name': record.partner_id.name if record.partner_id else False,
                } for record in sample_records],
                
                'partners': [{
                    'id': partner.id,
                    'name': partner.name,
                    'email': partner.email,
                    'phone': partner.phone,
                } for partner in partners],
                
                'sales': [{
                    'id': sale.id,
                    'name': sale.name,
                    'partner_id': sale.partner_id.id,
                    'amount_total': sale.amount_total,
                    'state': sale.state,
                } for sale in sales] if sales else []
            }
            
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            )
    
    @http.route('/api/related/records/<int:partner_id>', auth='public', type='http', methods=['GET'], csrf=False)
    def get_related_records(self, partner_id, **kwargs):
        try:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if not partner.exists():
                return Response(
                    json.dumps({'status': 'error', 'message': 'Partner not found'}),
                    content_type='application/json',
                    status=404
                )
            
            # Get related sample records (assuming there's a partner_id field in sample.record)
            related_samples = request.env['sample.record'].sudo().search([('partner_id', '=', partner_id)])
            
            # Get related sales orders
            related_sales = request.env['sale.order'].sudo().search([('partner_id', '=', partner_id)]) if 'sale.order' in request.env else []
            
            data = {
                'partner': {
                    'id': partner.id,
                    'name': partner.name,
                    'email': partner.email,
                    'phone': partner.phone,
                },
                'related_samples': [{
                    'id': record.id,
                    'name': record.name,
                    'state': record.state,
                    'amount': record.amount,
                } for record in related_samples],
                'related_sales': [{
                    'id': sale.id,
                    'name': sale.name,
                    'amount_total': sale.amount_total,
                    'state': sale.state,
                } for sale in related_sales] if related_sales else []
            }
            
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            ) 