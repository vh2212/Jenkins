from flask import make_response, abort
from config import db
from models import Person, PersonSchema, Note, NoteSchema

# se crea el manejador de lectura para GET
def read_all():
    # crear la lista de personas de la data
    people = Person.query.order_by(Person.lname).all()

    # serializar la data para la respuesta
    person_schema = PersonSchema(many=True)
    data = person_schema.dump(people)
    return data

def read_one(person_id):
    # obtener la persona de la lista de personas de la data
    person = (
        Person.query.filter(Person.person_id == person_id)
            .outerjoin(Note)
            .one_or_none()
    )

    if person is not None:
        # serializar la data para la respuesta
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data
    else:
        abort(
            404, "La persona con el id {person_id} no se encuentra".format(person_id=person_id)
        )

def create(person):
    fname = person.get("fname", None)
    lname = person.get("lname", None)

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )
    
    if existing_person is None:
        # crear una instancia de persona usando el esquema y pasando dentro de persona
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session)

        # agregar a la persona a la base de datos
        db.session.add(new_person)
        db.session.commit()

        # serializar y retornar la nueva persona creada
        #data = schema.dump(new_person)
        #return data, 201

        return make_response(
            "{lname} creado existosamente.".format(lname=lname), 201
        )
    else:
        abort(
            406,
            "La persona con el apellido {lname} ya existe.".format(lname=lname)
        )

def update(person_id, person):
    update_person = Person.query.filter(Person.person_id == person_id).one_or_none()
    
    fname = person.get("fname", None)
    lname = person.get("lname", None)

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    if update_person is None:
        abort(
            404, "La persona con el id {person_id} no se encuentra".format(person_id=person_id)
        )
    elif ( existing_person is not None and existing_person.person_id != person_id ):
        abort(
            408, "La persona con el apellido {lname} ya se encuentra".format(lname=lname)
        )
    else:
        # pasar la persona dentro del objeto de base de datos
        schema = PersonSchema()
        update = schema.load(person, session=db.session)

        # asignar el id para la persona que se quiere actualizar
        update.person_id = update_person.person_id

        # mezclar el nuevo objeto dentro del viejo y guardar en base de datos
        db.session.merge(update)
        db.session.commit()

        # serializar y retornar la nueva persona creada
        #data = schema.dump(update_person)
        #return data, 201

        return make_response(
            "{lname} actualizado existosamente.".format(lname=lname), 202
        )

def delete(person_id):
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is not None:
        db.session.delete(person)
        db.session.commit()
        
        return make_response(
            "{person_id} eliminado existosamente.".format(person_id=person_id), 202
        )
    else:
        abort(
            404, "La persona con el id {person_id} no se encuentra".format(person_id=person_id)
        )
