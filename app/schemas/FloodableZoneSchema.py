from marshmallow import Schema, fields, post_dump

def coordsFormatter(obj):
    raw_coords = obj.coords[1:-1].replace('[',' ').replace(']',' ').replace(',',' ').split()
    return  [{"lat": raw_coords[i]  , "long": raw_coords[i+1] } for i in range(0,len(raw_coords),2) ]


class FloodableZoneSchema(Schema):

    color= fields.Str()
    id= fields.Int(attribute="id_floodableZone")
    nombre= fields.Str(attribute="name")
    codigo_area = fields.Str(attribute="zone_code")
    coordenadas = fields.Function(lambda obj: coordsFormatter(obj))

    @post_dump
    def wrap_with_envelope(self, data, many, **kwargs):
        if (not many):
            key = "atributos"
            return {key: data}
        return data

class FloodableZonePaginationSchema(Schema):
    por_pagina = fields.Int(attribute="per_page")
    pagina = fields.Int(attribute="page")
    total = fields.Int()
    items = fields.Nested(FloodableZoneSchema, many=True, data_key="zonas")


fzones_schema = FloodableZonePaginationSchema()
fzone_schema = FloodableZoneSchema()
