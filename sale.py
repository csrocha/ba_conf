from openerp import models, fields, api
from openerp.osv import fields, osv

from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from datetime import date 



import logging
_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = 'sale.order'



    def copy(self, cr, uid, id, default=None, context=None):
        default['user_id']=uid


        company_pool = self.pool.get('res.company')
        company_id = company_pool._company_default_get(cr, uid)
        company = company_pool.browse(cr, uid,[company_id])

        today = date.today()

        date_validity = today + relativedelta( days=company.default_sale_order_validity_days)

        default['date_validity']=date_validity


        new_sale_order_id = super(sale_order, self).copy(cr, uid, id, default, context)


        order_line_obj = self.pool.get('sale.order.line')
        for sale in self.browse(cr, uid, [new_sale_order_id]):
            for line in sale.order_line:
                price = self.pool.get('product.pricelist').price_get(
                    cr, uid, [sale.pricelist_id.id],
                    line.product_id.id, line.product_uom_qty or 1.0,
                    sale.partner_id.id, {
                        'uom': line.product_uom.id,
                        'date': sale.date_order,
                    })[sale.pricelist_id.id]
                order_line_obj.write(cr, uid, [line.id], {'price_unit': price})
        return new_sale_order_id




    def update_prices_combo(self, cr,uid, ids, pricelist_id, order_lines,partner_id, context=None):
        context = context or {}

        res = super(sale_order, self).update_prices_combo(self, cr, uid, ids, pricelist_id, order_lines, partner_id, context=context)

        if not pricelist_id:
            return res
        
        lines=[]

        order_line_obj = self.pool.get('sale.order.line')

        def get_price(line_id):
            line = order_line_obj.browse(cr, uid,order_line[1])
            return self.pool.get('product.pricelist').price_get(
                        cr, uid, [pricelist_id],
                        line.product_id.id, line.product_uom_qty or 1.0,
                        partner_id, {
                            'uom': line.product_uom.id,
                        })[pricelist_id]

        lines = [{0: lambda ol: (ol[0], ol[1], dict(ol[2], **{'price_unit': get_price(ol[1])})),
                  1: lambda ol: (ol[0], ol[1], dict(ol[2], **{'price_unit': get_price(ol[1])})),
                  6: lambda ol: (1, ol[1], {'price_unit': get_price(ol[1])})
                  }.get(order_line[0], lambda ol: ol)(order_line)
                  for order_line in order_lines ]
                    
        res.value['order_line']=lines
        return res

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _columns = {

        'product_image': fields.related('product_id', 'image_medium', type='binary',relation="product.template" ,readonly=True , string='Product Image'),
        'product_description': fields.related('product_id', 'description', type='text',relation="product.template",readonly=True ,  string='Product Description'),
    }
sale_order_line()
