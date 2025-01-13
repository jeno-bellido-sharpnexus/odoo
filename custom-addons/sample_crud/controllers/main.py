from odoo import http
from odoo.http import request, Response
import json

class SampleAPI(http.Controller):
    def _build_cors_response(self, body, status=200):
        response = Response(
            json.dumps(body),
            content_type='application/json',
            status=status
        )
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    @http.route('/api/sample/records', auth='public', type='http', methods=['OPTIONS'], csrf=False)
    def options_records(self, **kwargs):
        return self._build_cors_response({'status': 'ok'})

    @http.route('/api/sample/records', auth='public', type='http', methods=['GET'], csrf=False)
    def get_records(self, **kwargs):
        try:
            sample_records = request.env['sample.record'].sudo().search([])
            
            data = {
                'records': [{
                    'id': record.id,
                    'icon': record.icon,
                    'name': record.name,
                    'phone': record.phone,
                    'email': record.email,
                    'status': record.status,
                    'address': record.address,
                    'repStatus': record.rep_status,
                    'promoRef': record.promo_ref,
                    'frequency': record.frequency,
                    'rollingFrequency': record.rolling_frequency,
                    'territory': record.territory,
                    'notes': record.notes,
                    'fax': record.fax,
                    'lat': record.latitude,
                    'lng': record.longitude,
                    'siteId': record.site_id,
                } for record in sample_records]
            }
            
            return self._build_cors_response({'status': 'success', 'data': data})
        except Exception as e:
            return self._build_cors_response({'status': 'error', 'message': str(e)}, 500)

    @http.route('/api/related/records/<int:partner_id>', auth='public', type='http', methods=['OPTIONS'], csrf=False)
    def options_related_records(self, **kwargs):
        return self._build_cors_response({'status': 'ok'})

    @http.route('/api/related/records/<int:partner_id>', auth='public', type='http', methods=['GET'], csrf=False)
    def get_related_records(self, partner_id, **kwargs):
        try:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if not partner.exists():
                return self._build_cors_response({'status': 'error', 'message': 'Partner not found'}, 404)
            
            related_samples = request.env['sample.record'].sudo().search([('partner_id', '=', partner_id)])
            
            data = {
                'partner': {
                    'id': partner.id,
                    'name': partner.name,
                    'email': partner.email,
                    'phone': partner.phone,
                },
                'related_samples': [{
                    'id': record.id,
                    'icon': record.icon,
                    'name': record.name,
                    'phone': record.phone,
                    'email': record.email,
                    'status': record.status,
                    'address': record.address,
                    'repStatus': record.rep_status,
                    'promoRef': record.promo_ref,
                    'frequency': record.frequency,
                    'rollingFrequency': record.rolling_frequency,
                    'territory': record.territory,
                    'notes': record.notes,
                    'fax': record.fax,
                    'lat': record.latitude,
                    'lng': record.longitude,
                    'siteId': record.site_id,
                } for record in related_samples]
            }
            
            return self._build_cors_response({'status': 'success', 'data': data})
        except Exception as e:
            return self._build_cors_response({'status': 'error', 'message': str(e)}, 500)

    @http.route('/api/sample/records/<int:record_id>', auth='public', type='http', methods=['OPTIONS'], csrf=False)
    def options_record_by_id(self, **kwargs):
        return self._build_cors_response({'status': 'ok'})

    @http.route('/api/sample/records/<int:record_id>', auth='public', type='http', methods=['GET'], csrf=False)
    def get_record_by_id(self, record_id, **kwargs):
        try:
            record = request.env['sample.record'].sudo().search([('id', '=', record_id)], limit=1)
            if not record:
                return self._build_cors_response({'status': 'error', 'message': 'Record not found'}, 404)
            
            data = {
                'id': record.id,
                'icon': record.icon,
                'name': record.name,
                'phone': record.phone,
                'email': record.email,
                'status': record.status,
                'address': record.address,
                'repStatus': record.rep_status,
                'promoRef': record.promo_ref,
                'frequency': record.frequency,
                'rollingFrequency': record.rolling_frequency,
                'territory': record.territory,
                'notes': record.notes,
                'fax': record.fax,
                'lat': record.latitude,
                'lng': record.longitude,
                'siteId': record.site_id,
            }
            
            return self._build_cors_response({'status': 'success', 'data': data})
        except Exception as e:
            return self._build_cors_response({'status': 'error', 'message': str(e)}, 500) 