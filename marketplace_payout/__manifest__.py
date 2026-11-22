{
    'name': 'Marketplace Payout',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Track and pay out what marketplace sellers are owed',
    'author': 'Soukaina Sabbaji',
    'license': 'LGPL-3',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/payout_payee_views.xml',
        'views/payout_menus.xml',
    ],
    'application': True,
}
