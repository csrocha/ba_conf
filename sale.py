from openerp import models, fields, api
from openerp.osv import fields, osv
from openerp.addons.sale import sale
from openerp.tools.translate import _

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    _columns = {

        'product_image': fields.related('product_id', 'image_medium', type='binary',relation="product.template" ,readonly=True , string='Product Image'),
        'product_description': fields.related('product_id', 'description', type='text',relation="product.template",readonly=True ,  string='Product Description'),
    }
sale_order_line()