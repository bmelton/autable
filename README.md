# Autable

Short for "auto-table", the idea is that you should be able to feed a set of values
into SQLAlchemy, then create the database schema from those values as sort of the opposite of introspection.

This should definitely not be used by anyone at this point, and is very much a toy.

I'll update this as the tool progresses. 

## Installation

In a virtualenvironment, `pip install -r requirements.txt`

## Usage

Define a schema. The schema should contain a classname and a table name, and an array of columns in basic types. (Only "string" and "integer" are currently validated, mapping to String and Integer column types, respectively.)

An 'id' field will be automatically created, because I just need it there. I'm sure there are good use cases for tables without an id column, but I can't imagine them in a context where you don't know what the data is.

```
schema = {
  "classname": "MyClassName",
  "tablename": "customer1-spreadsheet-1-3-12-2023",
  "columns": [
    {"name": "column1", "type": "string",
    {"name": "column2", "type": "integer",
  ]
}
```

Pass that in to `create_table_mapping`

Now you can map your input sources to a data array and insert into it like you ordinarily might usually do. 

Here's some example code, using the above schema: 

```
def main():
  MyClass = create_table_mapping(schema)
  data = [
    {"column1": "this is a string object", "column2": 500},
    {"column1": "this is a second string object", "column2": 900},
    {"column1": "this is a third string object", "column2": 100},
  ]

  engine = create_engine("sqlite:///temp.db", echo=True)
  Base.metadata.create_all(engine)
 
  # Insert all your data
  with Session(engine) as session:
    session.add_all(MyClass(**rec) for rec in data)
    session.commit()

  # To query the data
  with Session(engine) as session:
    results = session.query(MyClass).all()
    for result in results:
      print(result.id)
  
```

## TODO

* Add more table types
* Possibly derive data attributes from a given spreadsheet 
* ID column should be optional and/or optionally not be an Integer
