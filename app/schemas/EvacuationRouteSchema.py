from marshmallow import Schema, fields

def coordsFormatter(obj):
    raw_coords = obj.coords[1:-1].replace('[',' ').replace(']',' ').replace(',',' ').split()
    return  [{"lat": raw_coords[i]  , "long": raw_coords[i+1] } for i in range(0,len(raw_coords),2) ]


class  EvacuationRouteSchema(Schema):
    id= fields.Int(attribute="id_eRoute")
    nombre= fields.Str(attribute="name")
    descripcion = fields.Str(attribute="description")
    coordenadas = fields.Function(lambda obj: coordsFormatter(obj))
    color = fields.Str()

class EvacuationRoutePaginationSchema(Schema):
    por_pagina = fields.Int(attribute="per_page")
    pagina = fields.Int(attribute="page")
    total = fields.Int()
    items = fields.Nested(EvacuationRouteSchema, many=True, data_key="recorridos")


eroutes_schema = EvacuationRoutePaginationSchema()
