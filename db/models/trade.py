class BaseModel(Model):
  class Meta:
    database = db

class Trade(BaseModel):
  timestamp = TimestampField()
  side = TextField()
  size = IntegerField()
  price = DecimalField()
  tick_direction = TextField()