# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DocumentShipping(models.Model):
    _name = "document.shipping"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Valija"

    date_out = fields.Date(string="Fecha de Envío", default=fields.Date.today)
    date_in = fields.Date(string="Fecha de Recepción",)
    user_out_id = fields.Many2one(
        "res.users", 
        string="Emitido por", 
        default=lambda self: self.env.user
    )
    user_in_id = fields.Many2one("res.users", string="Recibido por", tracking= True,)
    user_send_id = fields.Many2one("res.users", string="Enviado a", tracking= True,)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )
    state = fields.Selection(
        [("draft", "Borrador"), ("done", "Realizado"),],
        string="Estado",
        readonly=True,
        tracking=True,
        default="draft",
    )
    type = fields.Selection(
        [("in", "Recepcion"), ("out", "Entrega"),],
        string="Tipo",
        readonly=True,
        tracking=True,
    )
    documents_ids = fields.One2many(
        "document.shipping.line", "document_id", "Documento"
    )
    name = fields.Char(string="Código", readonly=True)

    def action_ok(self):
        #if not self.documents_ids:
        #    raise UserError("Ingrese el detalle")
        if self.type == "in":
            self.name = self.env["ir.sequence"].next_by_code("document.shipping.in")
        if self.type == "out":
            self.name = self.env["ir.sequence"].next_by_code("document.shipping.out")
        self.state = "done"

class DocumentShippingType(models.Model):
    _name = "document.shipping.type"
    _description = "Tipo de Documento"

    name = fields.Char(string="Nombre")
    is_receipt_required = fields.Boolean(string="Requiere Nro Recibo?")

class DocumentShippingLine(models.Model):
    _name = "document.shipping.line"
    _description = "Detalle de valija"

    amount = fields.Float(string="Valor",)
    bank_id = fields.Many2one("res.bank", string="Entidad",)
    partner_id = fields.Many2one("res.partner", string="Cliente",)
    note = fields.Char(string="Nota")
    reference = fields.Char(string="Nro Documento")
    document_type_id = fields.Many2one("document.shipping.type", string="Documento",)
    document_id = fields.Many2one("document.shipping", string="Valija", readonly=True)
    num_receipt = fields.Char(string="Nro Recibo")

    @api.constrains('document_type_id', 'document_id.type')
    def _check_num_receipt_required(self):
        for line in self:
            if line.document_type_id.is_receipt_required and line.document_id.type == 'in':
                if not line.num_receipt:
                    raise ValidationError("El campo Nro Recibo es requerido.")
