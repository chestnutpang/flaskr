from flaskr.database import DbBase, db


class Bill(DbBase):
    __tablename__ = 'bill'
    record_type = db.Column(db.VARCHAR(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    alias = db.Column(db.VARCHAR(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    bill_mod = db.Column(db.Integer, db.ForeignKey('BillMod.id'))
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    record_time = db.Column(db.String(10), nullable=False)

    def __init__(self, record_type, amount, alias, user_id, times, bill_mod):
        self.record_type = record_type
        self.amount = amount
        self.alias = alias
        self.user_id = user_id
        self.bill_mod = bill_mod
        self.update_time(*times)

    def update_time(self, year, month, day):
        self.year = year
        self.month = month
        self.record_time = f'{year}-{month:0>2d}-{day:0>2d}'


class BillMod(DbBase):
    __tablename__ = 'bill'
    type = db.Column(db.VARCHAR(20), nullable=False)
    description = db.Column(db.VARCHAR(20), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, base_type='基本消费', amount=0, description=None):
        self.user_id = user_id
        self.type = base_type
        self.amount = amount
        self.description = description
