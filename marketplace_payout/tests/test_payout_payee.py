from psycopg2 import IntegrityError

from odoo.exceptions import AccessError, UserError
from odoo.tests import TransactionCase, new_test_user, tagged
from odoo.tools import mute_logger


@tagged('post_install', '-at_install')
class TestPayoutPayee(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Atlas Crafts'})
        cls.payee = cls.env['payout.payee'].create({'partner_id': cls.partner.id})
        cls.other_company = cls.env['res.company'].create({'name': 'Other Company'})

    def test_defaults(self):
        self.assertEqual(self.payee.company_id, self.env.company)
        self.assertEqual(self.payee.currency_id, self.env.company.currency_id)
        self.assertEqual(self.payee.display_name, 'Atlas Crafts')

    def test_partner_unique_per_company(self):
        self.payee.active = False
        with mute_logger('odoo.sql_db'), self.assertRaises(IntegrityError):
            self.env['payout.payee'].create({'partner_id': self.partner.id})

    def test_same_partner_in_other_company(self):
        payee = self.env['payout.payee'].create({
            'partner_id': self.partner.id,
            'company_id': self.other_company.id,
        })
        self.assertTrue(payee)

    def test_partner_of_other_company_rejected(self):
        foreign = self.env['res.partner'].create({
            'name': 'Foreign Seller',
            'company_id': self.other_company.id,
        })
        with self.assertRaises(UserError):
            self.env['payout.payee'].create({'partner_id': foreign.id})

    def test_regular_user_has_no_access(self):
        user = new_test_user(self.env, login='payout_outsider', groups='base.group_user')
        with self.assertRaises(AccessError):
            self.payee.with_user(user).read(['partner_id'])
