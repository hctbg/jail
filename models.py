import peewee


db = peewee.SqliteDatabase(
    'details.db',
    pragmas={'foreign_keys': 1}
)


class detainee_info(peewee.Model):
    detainee_id = peewee.CharField(primary_key=True)
    name = peewee.CharField()
    height = peewee.CharField()
    weight = peewee.CharField()
    sex = peewee.CharField()
    eyes = peewee.CharField()
    hair = peewee.CharField()
    race = peewee.CharField()
    age = peewee.IntegerField()
    city = peewee.CharField()
    state = peewee.CharField()

    class Meta:
        database = db


class charge(peewee.Model):
    detainee_id= peewee.CharField()
    case_num = peewee.CharField()
    description = peewee.CharField()
    status = peewee.CharField()
    bail_amount = peewee.CharField()
    bond_type = peewee.CharField()
    court_date = peewee.DateField()
    court_time = peewee.TimeField()
    jurisdiction = peewee.CharField()
    

    class Meta:
        database = db


db.connect()
db.create_tables([detainee_info, charge])