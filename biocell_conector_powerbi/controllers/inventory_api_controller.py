from odoo.http import Controller, route, request
from odoo.exceptions import ValidationError
import json
from datetime import date,datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)
class InventoryApiController(Controller):
    @route(['/api/inventory'], type='http', auth="public", website=False, csrf=False,  methods=['GET'])
    def _get_product_data(self, **kwargs):
        message=""
        try:
            header = request.httprequest.headers.get('Authorization')
            if not header or not header.startswith("Bearer "):
                raise ValidationError(f"Bearer token missing")
            token = header.split(" ")[1]
            required_token = request.env['powerbi.api.key'].sudo().search([
                ('name','=','inventory_api_powerbi')
            ])
            if token != required_token.token:
                raise ValidationError("Invalid Token")
            query=''.join(request.env['inventory.powerbi.api'].get_sql())
            request.env.cr.execute(query)
            message={
                "status": "success",
                "code": 200,
                "data": request.env.cr.dictfetchall()
            }
        except ValidationError as exception:
            message={
                "status": "Unauthorized",
                "message": str(exception),
                "code": 401
            }
        except Exception as exception:
            message={
                "error": "Odoo Server Error",
                "message": str(exception),
                "code": 500
            }
        return request.make_response(
            headers=[('Content-Type', 'application/json')],
            data=json.dumps(message,cls=CustomJSONEncoder)
        )