from marshmallow import Schema, fields

class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    due_date = fields.DateTime(allow_none=True)
