# models/rental.py
from odoo import models, fields, api
from datetime import datetime, timedelta

class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'
    _description = 'Alquiler de Producto'

    name = fields.Char(string='Referencia', required=True, copy=False, 
                      readonly=True, default='Nuevo')
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    producto_id = fields.Many2one('product.product', string='Producto', required=True)
    fecha_inicio = fields.Date(string='Fecha de Inicio', required=True, default=fields.Date.today)
    fecha_fin = fields.Date(string='Fecha de Fin', compute='_compute_fecha_fin', store=True)
    estado = fields.Selection([
        ('alquilado', 'En Alquiler'),
        ('entregado', 'Entregado'),
        ('no_entregado', 'No Entregado')
    ], string='Estado', default='alquilado', required=True)
    observaciones = fields.Text(string='Observaciones')
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('alquiler.producto') or 'Nuevo'
        return super(AlquilerProducto, self).create(vals)

    @api.depends('fecha_inicio')
    def _compute_fecha_fin(self):
        for alquiler in self:
            if alquiler.fecha_inicio:
                alquiler.fecha_fin = alquiler.fecha_inicio + timedelta(days=30)

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        if self.producto_id:
            # Verificar si el producto ya está alquilado
            alquiler_existente = self.search([
                ('producto_id', '=', self.producto_id.id),
                ('estado', '=', 'alquilado'),
            ])
            if alquiler_existente:
                return {
                    'warning': {
                        'title': 'Advertencia',
                        'message': 'Este producto ya está alquilado.'
                    }
                }

    def verificar_alquileres_vencidos(self):
        hoy = fields.Date.today()
        alquileres_vencidos = self.search([
            ('fecha_fin', '<', hoy),
            ('estado', '=', 'alquilado')
        ])
        alquileres_vencidos.write({'estado': 'no_entregado'})