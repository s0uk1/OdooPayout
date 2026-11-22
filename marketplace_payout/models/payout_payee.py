from odoo import fields, models


class PayoutPayee(models.Model):
    _name = 'payout.payee'
    _description = 'Payout Payee'
    _inherit = ['mail.thread']
    _rec_name = 'partner_id'
    _check_company_auto = True

    partner_id = fields.Many2one(
        'res.partner', required=True, ondelete='restrict', index=True,
        check_company=True, tracking=True,
    )
    company_id = fields.Many2one(
        'res.company', required=True, index=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency', required=True, tracking=True,
        default=lambda self: self.env.company.currency_id,
    )
    active = fields.Boolean(default=True)

    # Archived payees count too: a seller keeps a single history per company.
    _partner_company_uniq = models.Constraint(
        'UNIQUE(partner_id, company_id)',
        'This partner is already a payee in this company.',
    )
