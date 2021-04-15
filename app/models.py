from app import db
from sqlalchemy.dialects import mysql

class Fact(db.Model):
	pk_id = db.Column(db.Integer, primary_key = True)
	name = db.Column(mysql.VARCHAR(1000), nullable = False)
	fact = db.Column(mysql.VARCHAR(1000), nullable = False)

	def __repr__(self):
		return f'Fact(\'{self.name}\', \'{self.fact}\')'