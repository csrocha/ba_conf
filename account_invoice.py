from openerp import models, fields, api
from openerp.osv import fields, osv
from openerp.addons.sale import sale
from openerp.tools.translate import _


class account_invoice(osv.osv):
    _inherit = "account.invoice"

    _columns = {}


    def create(self, cr, uid, vals, context=None):
        account_journal=self.pool.get('account.journal')
        journal=account_journal.read(cr, uid, vals['journal_id'], ['section_id'])
        
        if 'section_id' in journal and journal['section_id']:
            vals['section_id']=journal['section_id'][0]

        return super(account_invoice, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        account_journal=self.pool.get('account.journal')
        if 'journal_id' in vals :
            journal=account_journal.read(cr, uid, vals['journal_id'], ['section_id'])
            if 'section_id' in journal and journal['section_id']:
                vals['section_id']=journal['section_id'][0]


        return super(account_invoice, self).write(cr, uid, ids, vals, context=context)


account_invoice()

