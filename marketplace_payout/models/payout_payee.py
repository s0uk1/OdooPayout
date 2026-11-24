from odoo import _, fields, models
from odoo.exceptions import UserError


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
    state = fields.Selection(
        [('draft', 'Draft'), ('verified', 'Verified'), ('blocked', 'Blocked')],
        required=True, default='draft', copy=False, index=True, tracking=True,
        readonly=True,
    )

    # Archived payees count too: a seller keeps a single history per company.
    _partner_company_uniq = models.Constraint(
        'UNIQUE(partner_id, company_id)',
        'This partner is already a payee in this company.',
    )

    def _check_state(self, allowed, action):
        wrong = self.filtered(lambda payee: payee.state not in allowed)
        if wrong:
            raise UserError(_(
                "You cannot %(action)s these payees: %(names)s",
                action=action, names=", ".join(wrong.mapped('display_name')),
            ))

    def action_verify(self):
        self._check_state({'draft'}, _('verify'))
        self.state = 'verified'

    def action_block(self):
        self._check_state({'draft', 'verified'}, _('block'))
        self.state = 'blocked'

    def action_reset_to_draft(self):
        # An unblocked payee must be verified again before being paid.
        self._check_state({'blocked'}, _('reset'))
        self.state = 'draft'
