from marshmallow import fields, Schema

from application.schemas.director import DirectorSchema
from application.schemas.genre import GenreSchema


class MovieSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    trailer = fields.Str(required=True)
    year = fields.Int(required=True)
    rating = fields.Float(required=True)
    director = fields.Nested(DirectorSchema)
    genre = fields.Nested(GenreSchema)
