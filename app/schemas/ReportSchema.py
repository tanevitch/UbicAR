from marshmallow import Schema, fields
from marshmallow.decorators import post_dump

def coordsFormatter(obj):
    raw_coords = obj.coords[1:-1].replace('[',' ').replace(']',' ').replace(',',' ').split()
    return  [raw_coords[0], raw_coords[1]]


class ReportSchema(Schema):
    categoria_id = fields.Int(attribute="category")
    apellido_denunciante = fields.Str(attribute="lname")
    nombre_denunciante = fields.Str(attribute="fname")
    telcel_denunciante = fields.Str(attribute="phone")
    email_denunciante = fields.Email(attribute="email")
    titulo= fields.Str(attribute="title")
    descripcion= fields.Str(attribute="description")

    @post_dump
    def wrap_with_envelope(self, data, many): #many es obligatorio para que no tire error, se lo manda igual
        key = "atributos"
        return {key: data}


class ReportPublicSchema(Schema):
    id= fields.Int(attribute="id_report")
    coordenadas = fields.Function(lambda obj: coordsFormatter(obj))
    titulo= fields.Str(attribute="title")
    estado= fields.Str(attribute="status")

class ReportPaginationSchema(Schema):
    por_pagina = fields.Int(attribute="per_page")
    pagina = fields.Int(attribute="page")
    total = fields.Int()
    items = fields.Nested(ReportPublicSchema, many=True, data_key="denuncias")

report_schema = ReportSchema()
reports_schema = ReportPaginationSchema()
