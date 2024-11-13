{
    'name': 'Document Shipping',
    'summary': """
        Document Shipping""",
    'description': """
        Document Shipping
    """,
    'author': 'Ismael Calle',
    'website': '',
    'category': 'Tools',
    'version': '18.0.0.1',
    'depends': ['account'],
    # always loaded
    'data': 
    [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/document_shipping_view.xml",
        "views/document_shipping_report.xml",
    ],
    'installable': True,
    'license': 'LGPL-3',
}