from marshmallow import Schema, fields

def coordsFormatter(obj):
    raw_coords = obj.coords[1:-1].replace('[',' ').replace(']',' ').replace(',',' ').split()
    return  [{"lat": raw_coords[i]  , "long": raw_coords[i+1] } for i in range(0,len(raw_coords),2) ]


class  MeetingPointSchema(Schema):
    id= fields.Int(attribute="id_point")
    nombre= fields.Str(attribute="name")
    direccion = fields.Str(attribute="address")
    coordenadas = fields.Function(lambda obj: coordsFormatter(obj))
    telefono = fields.Str(attribute="phone")
    email = fields.Str(attribute="mail")


class MeetingPointPaginationSchema(Schema):
    por_pagina = fields.Int(attribute="per_page")
    pagina = fields.Int(attribute="page")
    total = fields.Int()
    items = fields.Nested(MeetingPointSchema, many=True, data_key="puntos_encuentro")


mpoints_schema = MeetingPointPaginationSchema()
