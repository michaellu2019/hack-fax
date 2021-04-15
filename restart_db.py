from app import db
from app.models import Fact

db.session.rollback()
db.drop_all()
db.create_all()

default_facts = [{"name": "Michael", "fact": "Exceptionally mediocre."}, 
				 	  {"name": "Jianna", "fact": "Sweaty hands."}, 
				 	  {"name": "Allen", "fact": "Closeted communist."},
					  {"name": "Nat", "fact": "Half the size of Michael."},
					  {"name": "Jamie", "fact": "Scary lady (not as scary as Mindy though)."}]

for fact in default_facts:
	try:
		fact = Fact(name = fact["name"], fact = fact["fact"])
		db.session.add(fact)
		db.session.commit()
	except SQLAlchemyError as ex:
		db.session.rollback()
		print("Error creating default fact...")