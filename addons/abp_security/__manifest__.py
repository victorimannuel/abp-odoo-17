{
    'name': 'Able Pack Security',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Security',
    'version': '17.0',
    'description': """
    """,
    'depends': [
        'base',
        'mail',
        'calendar',
        'contacts',
        'crm',
        'sale',
        'abp_salesperson_dashboard',
        'abp_customer_catalogue',
        'spreadsheet_dashboard',
        'sale_subscription',
        'point_of_sale',
        'account_accountant',
        'documents',
        'website',
        'purchase',
        'stock',
        'mrp',
        'mrp_workorder',
        'sign',
        'hr',
        'hr_work_entry_contract_enterprise',
        'hr_expense',
        'utm',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}