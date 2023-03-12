# Autable

Short for "auto-table", the idea is that you should be able to feed a set of values
into SQLAlchemy, then create the database schema from those values as sort of the opposite of introspection.

This should definitely not be used by anyone at this point, and is very much a toy.

I'll update this as the tool progresses.

The basic ideas is that we're trying to extract data from spreadsheets and store it. There is already a system in place that will take a spreadsheet and allow users to specify things like "this column is populated with strings," and "this column is populated with integers" (still need to figure out datetimes, but that'll need a conversation.)

If we can convert that mapping data into a simple, storable JSON, then we can persist the table definition for later use in querying as well as to create the ORM model (which yields the side benefit of creating the table,) persist data from the spreadsheet to the table, and we can then feather back in the schema definition for result mapping. 

### Disclaimer: I haven't fact-checked any of the claims made in this README, and don't intend to. If it doesn't work, feel free to submit a PR. 

## Installation

In a virtualenvironment, `pip install -r requirements.txt`

## Usage

Define a schema. The schema should contain a classname and a table name, and an array of columns in basic types. (Only "string" and "integer" are currently validated, mapping to String and Integer column types, respectively.)

If you pass "id_field='auto'" (or nothing, it's the default) then it'll add an auto-incrementing Integer field named `id`. It's not there yet, but I plan to expand that into including other options like `None` to omit it completely. Otherwise, you can define a column with `"pk": True` in your column and that make that the primary key. 

Note: I'm not presently doing any validations whether or not there is more than one `pk` attribute per schema, so just try not to screw that up. There also aren't any short-term plans for adding anything like composite keys or anything, so if you need something like that, roll your own. 


Here's an example of a schema with an auto-incrementing `id` field:

```
schema = {
  "classname": "MyClassName",
  "tablename": "customer1-spreadsheet-1-3-12-2023",
  "columns": [
    {"name": "column1", "type": "string"},
    {"name": "column2", "type": "integer"},
  ]
}
```

Here's an example of a schema with a manually defined `id`:

```
schema = {
  "classname": "MyClassName",
  "tablename": "customer1-spreadsheet-1-3-12-2023",
  "columns": [
    {"name": "id", "type": "integer", "pk": True},
    {"name": "column1", "type": "string"},
    {"name": "column2", "type": "integer"},
  ]
}
```

Pass that in to `create_table_from_schema`

Now you can map your input sources to a data array and insert into it like you ordinarily might usually do. 

Here's some example code, using the above schema: 

```
def main():
  MyClass = create_table_from_schema(schema)
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

* Support for more generic table types
  - BigInteger
  - Boolean
  - Date
  - DateTime
  - Enum
  - Float
  - Interval
  - Numeric 
  - PickleType 
  - SmallInteger 
  - Text 
  - Time 
  - Unicode 
  - UnicodeText 
* Possibly derive data attributes from a given spreadsheet 
* ID column should be optional and/or optionally not be an Integer
