from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import cross_origin
import random

from app import app, db
from app.models import Fact

@app.route("/")
def home():
	return "Bruh go to the API..."

@app.route("/api/facts", methods = ["GET"])
def facts():
	facts = []

	facts_data = Fact.query.all();
	for fact_data in facts_data:
		facts.append({"id": fact_data.pk_id, "name": fact_data.name, "fact": fact_data.fact})

	return jsonify({"status": "success", "msg": "found fact data", "data": {"facts": facts}})

@app.route("/api/random-fact", methods = ["GET"])
def random_facts():
	facts = []

	facts_data = Fact.query.all();
	for fact_data in facts_data:
		facts.append({"id": fact_data.pk_id, "name": fact_data.name, "fact": fact_data.fact})
		
	return jsonify({"status": "success", "msg": "found fact data", "data": {"fact": facts[random.randint(0, len(facts) - 1)]}})

@app.route("/api/create-fact", methods = ["POST"])
def create_fact():
	fact_dict = request.get_json()["fact"]
	try:
		fact_data = Fact(name = fact_dict["name"], fact = fact_dict["fact"])
		db.session.add(fact_data)
		db.session.commit()
		fact = {
			"id": fact_data.pk_id,
			"name": fact_data.name,
			"fact": fact_data.fact
		}

		return jsonify({"status": "success", "msg": "created fact data", "data": {"fact": fact}})
	except SQLAlchemyError as ex:
		db.session.rollback()
		print("Error creating fact...")
		return jsonify({"status": "fail", "msg": "failed to create fact", "data": {}})

@app.route("/api/update-fact", methods = ["POST"])
def update_fact():
	fact_dict = request.get_json()["fact"]
	fact_data = Fact.query.filter_by(pk_id = fact_dict["id"]).first()
	if fact_data:
		try:
			fact_data.fact = fact_dict["fact"]
			db.session.commit()
			fact = {
				"id": fact_data.pk_id,
				"name": fact_data.name,
				"fact": fact_data.fact
			}

			return jsonify({"status": "success", "msg": "updated fact data", "data": {"fact": fact}})
		except SQLAlchemyError as ex:
			db.session.rollback()
			print("Error updating fact...")
			return jsonify({"status": "fail", "msg": "failed to update fact", "data": {}})

	return jsonify({"status": "fail", "msg": "unidentified fact", "data": {}})