from flaskr.database import DbBase, db


class Bill(DbBase):
    __tablename__ = 'bill'
    record_type = db.Column(db.VARCHAR(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    alias = db.Column(db.VARCHAR(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    record_time = db.Column(db.String(10), nullable=False)

    def __init__(self, record_type, amount, alias, user_id, times):
        self.record_type = record_type
        self.amount = amount
        self.alias = alias
        self.user_id = user_id
        self.update_time(*times)

    def update_time(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.record_time = f'{year}-{month:0>2d}-{day:0>2d}'
