from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

_column_types = {
  "integer": Integer, 
  "string": String
}


def create_table_mapping(schema):
    clsdict = { "__tablename__": schema["tablename"] }

    # Add an 'id' field. Every table should have an id.
    clsdict.update({
        "id": Column(Integer, primary_key=True)
    })
    for rec in schema["columns"]:
        clsdict.update({
            rec["name"]: Column(
                _column_types[rec["type"]], primary_key=rec.get("is_pk", False)
            )
        })
    return type(schema["classname"], (Base, ), clsdict)


if __name__ == "__main__":
    schema = {
        "classname": "MyClass",
        "tablename": "my_table",
        "columns": [
            {"name": "column1", "type": "string"},
            {"name": "column2", "type": "integer"},
        ],
    }
    MyClass = create_table_mapping(schema)
    engine =  create_engine("sqlite:///temp.db", echo=False)
    Base.metadata.create_all(engine)

    data = [
        {"column1": "This is a record", "column2": 100},
        {"column1": "This is another record", "column2": 300},
        {"column1": "Wow. A third record", "column2": 200},
    ]

    with Session(engine) as session:
        session.add_all(MyClass(**rec) for rec in data)
        results = session.query(MyClass).all()
        for result in results:
            print(result.id, " :: ", result.column1)
        session.commit()
