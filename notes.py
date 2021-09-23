from flask import make_response, abort
from config import db
from models import Person, PersonSchema, Note, NoteSchema

# se crea el manejador de lectura para GET
def read_all():
    # crear la lista de personas de la data
    notes = Note.query.order_by(db.desc(Note.timestamp)).all()

    # serializar la data para la respuesta
    #note_schema = NoteSchema(many=True, exclude=["person.notes"])
    note_schema = NoteSchema(many=True)
    data = note_schema.dump(notes)
    return data

def read_one(person_id, note_id):
    # obtener la persona de la lista de personas de la data
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
            .filter(Person.person_id == person_id)
            .filter(Note.note_id == note_id)
            .one_or_none()
    )

    if note is not None:
        # serializar la data para la respuesta
        note_schema = NoteSchema()
        data = note_schema.dump(note)
        return data
    else:
        abort(
            404, "La nota con el id de persona {person_id} y nota {note_id} no se encuentra".format(person_id=person_id,note_id=note_id)
        )

def create(person_id, note):
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is None:
        abort(
            404, "La persona con el id {person_id} no se encuentra".format(person_id=person_id)
        )

    # crear una instancia de persona usando el esquema y pasando dentro de persona
    schema = NoteSchema()
    new_note = schema.load(note, session=db.session)

    # agregar a la persona a la base de datos
    #db.session.add(new_note)
    person.notes.append(new_note)
    db.session.commit()

    # serializar y retornar la nueva persona creada
    #data = schema.dump(new_note)
    #return data, 201

    return make_response(
        "Nota creado existosamente.", 201
    )

def update(person_id, note_id, note):
    update_note = (
        Note.query.filter(Person.person_id == person_id)
            .filter(Note.note_id == note_id)
            .one_or_none()
    )

    if update_note is not None:
        # pasar la persona dentro del objeto de base de datos
        schema = NoteSchema()
        update = schema.load(note, session=db.session)

        # asignar el id para la persona que se quiere actualizar
        update.note_id = update_note.note_id

        # mezclar el nuevo objeto dentro del viejo y guardar en base de datos
        db.session.merge(update)
        db.session.commit()

        # serializar y retornar la nueva persona creada
        #data = schema.dump(update_note)
        #return data, 201

        return make_response(
            "{note_id} actualizado existosamente.".format(note_id=note_id), 202
        )
    else:
        abort(
            404, "La nota con el id de persona {person_id} y nota {note_id} no se encuentra".format(person_id=person_id,note_id=note_id)
        )

def delete(person_id, note_id):
    note = (
        Note.query.filter(Person.person_id == person_id)
            .filter(Note.note_id == note_id)
            .one_or_none()
    )

    if note is not None:
        db.session.delete(note)
        db.session.commit()
        
        return make_response(
            "{note_id} eliminado existosamente.".format(note_id=note_id), 202
        )
    else:
        abort(
            404, "La nota con el id de persona {person_id} y nota {note_id} no se encuentra".format(person_id=person_id,note_id=note_id)
        )
