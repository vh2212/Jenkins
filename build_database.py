import os
from datetime import datetime
from config import db
from models import Person, Note

# Data
PEOPLE = [
    { "fname": "Victor", "lname": "Hernandez",
        "notes": [
            ("Primera nota", "2020-02-12 22:15:45"),
            ("Segunda nota", "2020-02-12 22:15:45")
        ]
    },
    { "fname": "Zayra", "lname": "Trujillo",
        "notes": [
            ("Primera nota", "2020-02-12 22:15:45"),
            ("Segunda nota", "2020-02-12 22:15:45")
        ]
    },
    { "fname": "Juana", "lname": "Robles",
        "notes": [
            ("Primera nota", "2020-02-12 22:15:45"),
            ("Segunda nota", "2020-02-12 22:15:45")
        ]
    }
]

# borrar el archivo base de datos si existe actualmente
dirname = os.path.abspath(os.path.dirname(__file__))
if os.path.exists(dirname+"/people.db"):
    os.remove(dirname+"/people.db")

# crear la base de datos
db.create_all()

# iterar sobre la estructura y poblar la base de datos
for person in PEOPLE:
    p = Person(lname=person.get("lname"), fname=person.get("fname"))

    # agregar las notas para la persona
    for note in person.get("notes"):
        content, timestamp = note
        p.notes.append(
            Note(
                content=content,
                timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            )
        )

    db.session.add(p)

db.session.commit()
