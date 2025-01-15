from functools import wraps
from odoo.http import Response, request

def cors(methods=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Handle preflight requests
            if request.httprequest.method == 'OPTIONS':
                headers = {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PATCH, DELETE',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Max-Age': '3600',
                    'Content-Type': 'text/plain'
                }
                return Response(status=200, headers=headers)

            # Handle actual request
            response = f(*args, **kwargs)
            if not isinstance(response, Response):
                response = Response(response)

            # Add CORS headers to response
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PATCH, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Credentials': 'true'
            }
            response.headers.update(headers)
            return response

        return wrapped
    return decorator 