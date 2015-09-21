from openerp import models, fields, api
from    openerp import  exceptions      
from openerp.osv import fields, osv
from openerp.addons.sale import sale
from openerp.tools.translate import _



class account_journal(osv.osv):
    _inherit = "account.journal"

    _columns = {
        'section_id':fields.many2one('crm.case.section', 'Sales Team')
    }

    
account_journal()


class account_journal_section_wizard(osv.osv_memory):
        _name = 'account.journal.section.wizard'
        _columns = {'section_id' : fields.many2one('crm.case.section', 'Sales Team'),
                    'point_of_sale' : fields.integer(string='Punto de venta')
                    }
        _defaults= {}

        def do_set_section(self, cr, uid,ids,context=None):

            journal=self.read(cr, uid, ids[0], ['section_id','point_of_sale'])
            cr.execute("""update account_journal set section_id=%s where point_of_sale=%s """,
                       (journal['section_id'][0],journal['point_of_sale']))

            return  {}

