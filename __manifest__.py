# __manifest__.py
{
    'name': 'Alquiler de Productos',
    'version': '1.0',
    'category': 'Ventas',
    'summary': 'Gestión de alquiler de productos para clientes registrados',
    'description': """
        Módulo para gestionar alquileres de productos en ElectroWord:
        - Asignar alquileres a clientes
        - Controlar disponibilidad de productos
        - Gestionar fechas de alquiler
        - Monitorizar estado de alquileres
    """,
    'depends': ['base', 'product', 'sale'],
    'data': [
        'security/rental_security.xml',
        'security/ir.model.access.csv',
        'views/rental_views.xml',
        'data/rental_cron.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
}