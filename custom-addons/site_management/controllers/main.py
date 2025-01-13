from odoo import http
from odoo.http import request, Response
import json
from ..utils import cors

class SiteAPI(http.Controller):
    # GET all sites
    @http.route('/api/sites', type='http', auth='public', methods=['GET', 'POST', 'OPTIONS'], csrf=False)
    @cors(['GET', 'POST', 'OPTIONS'])
    def get_sites(self, **kwargs):
        if request.httprequest.method == 'POST':
            return self.create_site(**kwargs)
            
        sites = request.env['site.site'].sudo().search([])
        result = [{'id': site.id, 'icon': site.icon or '🏪', 'name': site.name, 
                   'contacts': len(site.contact_ids), 'address': site.address or '', 
                   'city': site.city or '', 'phone': site.phone or '', 
                   'email': site.email or '', 'status': site.status or 'green'}
                  for site in sites]
        return Response(
            json.dumps({'status': 'success', 'data': result}),
            content_type='application/json'
        )

    # GET all contacts
    @http.route('/api/contacts', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    @cors(['GET'])
    def get_contacts(self, **kwargs):
        contacts = request.env['site.contact'].sudo().search([])
        result = [{'id': contact.id, 'icon': contact.icon or '👤', 'name': contact.name,
                   'phone': contact.phone or '', 'email': contact.email or '', 
                   'status': contact.status or 'green', 'address': contact.address or '', 
                   'repStatus': contact.rep_status or 'Active', 'promoRef': contact.promo_ref or '', 
                   'frequency': contact.frequency or 0, 'rollingFrequency': contact.rolling_frequency or '0 Days', 
                   'territory': contact.territory or '', 'notes': contact.notes or '', 
                   'fax': contact.fax or '', 'lat': contact.latitude or 0.0, 
                   'lng': contact.longitude or 0.0, 'siteId': contact.site_id.id}
                  for contact in contacts]
        return Response(
            json.dumps({'status': 'success', 'data': result}),
            content_type='application/json'
        )

    # GET contacts for a specific site
    @http.route('/api/sites/<int:site_id>/contacts', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    @cors(['GET'])
    def get_site_contacts(self, site_id, **kwargs):
        site = request.env['site.site'].sudo().browse(site_id)
        if not site.exists():
            return Response(
                json.dumps({'status': 'error', 'message': 'Site not found'}),
                content_type='application/json',
                status=404
            )
        
        result = [{'id': contact.id, 'icon': contact.icon or '👤', 'name': contact.name,
                   'phone': contact.phone or '', 'email': contact.email or '', 
                   'status': contact.status or 'green', 'address': contact.address or '', 
                   'repStatus': contact.rep_status or 'Active', 'promoRef': contact.promo_ref or '', 
                   'frequency': contact.frequency or 0, 'rollingFrequency': contact.rolling_frequency or '0 Days', 
                   'territory': contact.territory or '', 'notes': contact.notes or '', 
                   'fax': contact.fax or '', 'lat': contact.latitude or 0.0, 
                   'lng': contact.longitude or 0.0, 'siteId': contact.site_id.id}
                  for contact in site.contact_ids]
        return Response(
            json.dumps({'status': 'success', 'data': result}),
            content_type='application/json'
        )

    def create_site(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data.decode())
            required_fields = ['name']
            for field in required_fields:
                if not data.get(field):
                    return Response(
                        json.dumps({'status': 'error', 'message': f'Missing required field: {field}'}),
                        content_type='application/json',
                        status=400
                    )

            site_values = {
                'name': data.get('name'),
                'icon': data.get('icon', '🏪'),
                'address': data.get('address'),
                'city': data.get('city'),
                'phone': data.get('phone'),
                'email': data.get('email'),
                'status': data.get('status', 'green')
            }
            new_site = request.env['site.site'].sudo().create(site_values)
            return Response(
                json.dumps({'status': 'success', 'data': {
                    'id': new_site.id, 'icon': new_site.icon, 'name': new_site.name,
                    'contacts': len(new_site.contact_ids), 'address': new_site.address or '',
                    'city': new_site.city or '', 'phone': new_site.phone or '',
                    'email': new_site.email or '', 'status': new_site.status
                }}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            )
