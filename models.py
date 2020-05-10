import peewee


db = peewee.SqliteDatabase(
    'details.db',
    pragmas={'foreign_keys': 1}
)


class detainee_info(peewee.Model):
    detainee_id =peewee.CharField(primary_key=True) 
    name = peewee.CharField() 
    height = peewee.CharField()
    weight = peewee.CharField()
    eyes = peewee.CharField()
    hair = peewee.CharField()
    race = peewee.CharField()
    age  = peewee.CharField()
    city = peewee.CharField()
    state = peewee.CharField()

    class Meta:
        database = db


class charge(peewee.Model):
    detainee_id = peewee.ForeignKeyField(
        detainee_info,
        backref='charge',
        column_name='detainee_id',
    )
    case_num = peewee.IntegerField()
    description = peewee.CharField()
    status = peewee.CharField()
    bail_amount = peewee.CharField()
    bond_type = peewee.CharField()
    court_date = peewee.CharField()
    court_time = peewee.CharField()
    jurisdiction = peewee.CharField()
    driver_city_state = peewee.CharField()
    driver_insurance = peewee.CharField()
    direction = peewee.CharField()

    class Meta:
        database = db
        primary_key = peewee.CompositeKey(
            'detainee_id', 'case_num'
        )


db.connect()
db.create_tables([detainee_info, charge])