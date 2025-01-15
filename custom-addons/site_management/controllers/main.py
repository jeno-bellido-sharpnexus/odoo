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
    @http.route('/api/contacts', type='http', auth='public', methods=['GET', 'POST', 'OPTIONS'], csrf=False)
    @cors(['GET', 'POST'])
    def get_contacts(self, **kwargs):
        if request.httprequest.method == 'POST':
            return self.create_contact(**kwargs)
            
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

    # GET a specific site
    @http.route('/api/sites/<int:site_id>', type='http', auth='public', methods=['GET', 'PATCH', 'DELETE', 'OPTIONS'], csrf=False)
    @cors(['GET', 'DELETE'])
    def get_site(self, site_id, **kwargs):
        if request.httprequest.method == 'DELETE':
            return self.delete_site(site_id, **kwargs)
            
        site = request.env['site.site'].sudo().browse(site_id)
        if not site.exists():
            return Response(
                json.dumps({'status': 'error', 'message': 'Site not found'}),
                content_type='application/json',
                status=404
            )
        
        result = {
            'id': site.id, 
            'icon': site.icon or '🏪', 
            'name': site.name,
            'contacts': len(site.contact_ids), 
            'address': site.address or '', 
            'city': site.city or '', 
            'phone': site.phone or '', 
            'email': site.email or '', 
            'status': site.status or 'green'
        }
        return Response(
            json.dumps({'status': 'success', 'data': result}),
            content_type='application/json'
        )

    # GET a specific contact
    @http.route('/api/contacts/<int:contact_id>', type='http', auth='public', methods=['GET', 'DELETE', 'OPTIONS'], csrf=False)
    @cors(['GET', 'DELETE'])
    def get_contact(self, contact_id, **kwargs):
        if request.httprequest.method == 'DELETE':
            return self.delete_contact(contact_id, **kwargs)
            
        contact = request.env['site.contact'].sudo().browse(contact_id)
        if not contact.exists():
            return Response(
                json.dumps({'status': 'error', 'message': 'Contact not found'}),
                content_type='application/json',
                status=404
            )
        
        result = {
            'id': contact.id, 
            'icon': contact.icon or '👤', 
            'name': contact.name,
            'phone': contact.phone or '', 
            'email': contact.email or '', 
            'status': contact.status or 'green', 
            'address': contact.address or '', 
            'repStatus': contact.rep_status or 'Active', 
            'promoRef': contact.promo_ref or '', 
            'frequency': contact.frequency or 0, 
            'rollingFrequency': contact.rolling_frequency or '0 Days', 
            'territory': contact.territory or '', 
            'notes': contact.notes or '', 
            'fax': contact.fax or '', 
            'lat': contact.latitude or 0.0, 
            'lng': contact.longitude or 0.0, 
            'siteId': contact.site_id.id
        }
        return Response(
            json.dumps({'status': 'success', 'data': result}),
            content_type='application/json'
        )

    # DELETE a specific contact
    def delete_contact(self, contact_id, **kwargs):
        try:
            contact = request.env['site.contact'].sudo().browse(contact_id)
            if not contact.exists():
                return Response(
                    json.dumps({'status': 'error', 'message': 'Contact not found'}),
                    content_type='application/json',
                    status=404
                )
            
            contact.unlink()
            return Response(
                json.dumps({'status': 'success', 'message': 'Contact deleted successfully'}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            )

    # CREATE a new site
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

    # DELETE a specific site
    @http.route('/api/sites/<int:site_id>', type='http', auth='public', methods=['DELETE', 'OPTIONS'], csrf=False)
    @cors(['DELETE'])
    def delete_site(self, site_id, **kwargs):
        try:
            site = request.env['site.site'].sudo().browse(site_id)
            if not site.exists():
                return Response(
                    json.dumps({'status': 'error', 'message': 'Site not found'}),
                    content_type='application/json',
                    status=404
                )
            
            site.unlink()
            return Response(
                json.dumps({'status': 'success', 'message': 'Site deleted successfully'}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            )

    # CREATE a new contact
    def create_contact(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data.decode())
            required_fields = ['name', 'siteId']
            for field in required_fields:
                if not data.get(field):
                    return Response(
                        json.dumps({'status': 'error', 'message': f'Missing required field: {field}'}),
                        content_type='application/json',
                        status=400
                    )

            # Verify site exists
            site = request.env['site.site'].sudo().browse(int(data.get('siteId')))
            if not site.exists():
                return Response(
                    json.dumps({'status': 'error', 'message': 'Site not found'}),
                    content_type='application/json',
                    status=404
                )

            contact_values = {
                'name': data.get('name'),
                'icon': data.get('icon', '👤'),
                'phone': data.get('phone'),
                'email': data.get('email'),
                'status': data.get('status', 'green'),
                'address': data.get('address'),
                'rep_status': data.get('repStatus', 'Active'),
                'promo_ref': data.get('promoRef'),
                'frequency': data.get('frequency', 0),
                'rolling_frequency': data.get('rollingFrequency', '0 Days'),
                'territory': data.get('territory'),
                'notes': data.get('notes'),
                'fax': data.get('fax'),
                'latitude': data.get('lat', 0.0),
                'longitude': data.get('lng', 0.0),
                'site_id': site.id
            }
            new_contact = request.env['site.contact'].sudo().create(contact_values)
            return Response(
                json.dumps({'status': 'success', 'data': {
                    'id': new_contact.id,
                    'icon': new_contact.icon,
                    'name': new_contact.name,
                    'phone': new_contact.phone or '',
                    'email': new_contact.email or '',
                    'status': new_contact.status,
                    'address': new_contact.address or '',
                    'repStatus': new_contact.rep_status,
                    'promoRef': new_contact.promo_ref or '',
                    'frequency': new_contact.frequency,
                    'rollingFrequency': new_contact.rolling_frequency,
                    'territory': new_contact.territory or '',
                    'notes': new_contact.notes or '',
                    'fax': new_contact.fax or '',
                    'lat': new_contact.latitude,
                    'lng': new_contact.longitude,
                    'siteId': new_contact.site_id.id
                }}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            )

    # UPDATE a specific site
    @http.route('/api/sites/<int:site_id>', type='http', auth='public', methods=['PATCH', 'OPTIONS'], csrf=False)
    @cors(['PATCH'])
    def update_site(self, site_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data.decode())
            site = request.env['site.site'].sudo().browse(site_id)
            if not site.exists():
                return Response(
                    json.dumps({'status': 'error', 'message': 'Site not found'}),
                    content_type='application/json',
                    status=404
                )

            # Update site fields
            site.write({
                'name': data.get('name', site.name),
                'icon': data.get('icon', site.icon),
                'address': data.get('address', site.address),
                'city': data.get('city', site.city),
                'phone': data.get('phone', site.phone),
                'email': data.get('email', site.email),
                'status': data.get('status', site.status)
            })

            return Response(
                json.dumps({'status': 'success', 'data': {
                    'id': site.id, 'icon': site.icon, 'name': site.name,
                    'contacts': len(site.contact_ids), 'address': site.address or '',
                    'city': site.city or '', 'phone': site.phone or '',
                    'email': site.email or '', 'status': site.status
                }}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            )

    # UPDATE a specific contact
    @http.route('/api/contacts/<int:contact_id>', type='http', auth='public', methods=['PATCH', 'OPTIONS'], csrf=False)
    @cors(['PATCH'])
    def update_contact(self, contact_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data.decode())
            contact = request.env['site.contact'].sudo().browse(contact_id)
            if not contact.exists():
                return Response(
                    json.dumps({'status': 'error', 'message': 'Contact not found'}),
                    content_type='application/json',
                    status=404
                )

            # Update contact fields
            contact.write({
                'name': data.get('name', contact.name),
                'icon': data.get('icon', contact.icon),
                'phone': data.get('phone', contact.phone),
                'email': data.get('email', contact.email),
                'status': data.get('status', contact.status),
                'address': data.get('address', contact.address),
                'rep_status': data.get('repStatus', contact.rep_status),
                'promo_ref': data.get('promoRef', contact.promo_ref),
                'frequency': data.get('frequency', contact.frequency),
                'rolling_frequency': data.get('rollingFrequency', contact.rolling_frequency),
                'territory': data.get('territory', contact.territory),
                'notes': data.get('notes', contact.notes),
                'fax': data.get('fax', contact.fax),
                'latitude': data.get('lat', contact.latitude),
                'longitude': data.get('lng', contact.longitude),
                'site_id': data.get('siteId', contact.site_id.id)
            })

            return Response(
                json.dumps({'status': 'success', 'data': {
                    'id': contact.id,
                    'icon': contact.icon,
                    'name': contact.name,
                    'phone': contact.phone or '',
                    'email': contact.email or '',
                    'status': contact.status,
                    'address': contact.address or '',
                    'repStatus': contact.rep_status,
                    'promoRef': contact.promo_ref or '',
                    'frequency': contact.frequency,
                    'rollingFrequency': contact.rolling_frequency,
                    'territory': contact.territory or '',
                    'notes': contact.notes or '',
                    'fax': contact.fax or '',
                    'lat': contact.latitude,
                    'lng': contact.longitude,
                    'siteId': contact.site_id.id
                }}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=500
            )
