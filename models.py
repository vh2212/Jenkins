from datetime import datetime

from sqlalchemy.orm import backref
from config import db, ma
from marshmallow import fields

class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.relationship(
        'Note',
        backref='person',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Note.timestamp)'
    )

class Note(db.Model):
    __tablename__ = "note"
    note_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#class PersonSchema(ma.ModelSchema): ## flask-marshmallow < 0.12
class PersonSchema(ma.SQLAlchemyAutoSchema): ## flask-marshmallow > 0.12
    class Meta:
        model = Person #
        sqla_session = db.session #
        include_relationships = True
        load_instance = True
    notes = fields.Nested('PersonNoteSchema', default=[], many=True)

class PersonNoteSchema(ma.SQLAlchemyAutoSchema):
    note_id = fields.Int()
    person_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        sqla_session = db.session
        include_relationships = True
        load_instance = True
    person = fields.Nested('NotePersonSchema', default=None)

class NotePersonSchema(ma.SQLAlchemyAutoSchema):
    person_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.Str()