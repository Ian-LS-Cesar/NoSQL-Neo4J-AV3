from fastapi import FastAPI, HTTPException
from database import db
from models import (
	PersonCreate,
	PersonUpdate,
	CompanyCreate,
	CompanyUpdate,
	RelationshipCreate,
)
import uuid


api = FastAPI()


@api.on_event("shutdown")
def shutdown():
	# Close neo4j driver
	try:
		db.close()
	except Exception:
		pass


# ---------------------- Persons CRUD ----------------------


@api.post("/persons")
def create_person(payload: PersonCreate):
	person_id = str(uuid.uuid4())
	query = """
	CREATE (p:Person {id:$id, name:$name, age:$age, email:$email})
	RETURN properties(p) AS person
	"""
	params = {"id": person_id, "name": payload.name, "age": payload.age, "email": payload.email}
	res = db.execute_write(query, params)
	return res[0].get("person") if res else None


@api.get("/persons/{person_id}")
def get_person(person_id: str):
	query = "MATCH (p:Person {id:$id}) RETURN properties(p) AS person LIMIT 1"
	res = db.execute_read(query, {"id": person_id})
	if not res:
		raise HTTPException(status_code=404, detail="Person not found")
	return res[0].get("person")


@api.get("/persons")
def list_persons():
	query = "MATCH (p:Person) RETURN properties(p) AS person"
	res = db.execute_read(query)
	return [r.get("person") for r in res]


@api.put("/persons/{person_id}")
def update_person(person_id: str, payload: PersonUpdate):
	props = {k: v for k, v in payload.dict().items() if v is not None}
	if not props:
		raise HTTPException(status_code=400, detail="No fields to update")
	query = "MATCH (p:Person {id:$id}) SET p += $props RETURN properties(p) AS person"
	res = db.execute_write(query, {"id": person_id, "props": props})
	if not res:
		raise HTTPException(status_code=404, detail="Person not found")
	return res[0].get("person")


@api.delete("/persons/{person_id}")
def delete_person(person_id: str):
	query = "OPTIONAL MATCH (p:Person {id:$id}) WITH p, p IS NOT NULL AS exists DETACH DELETE p RETURN exists AS deleted"
	res = db.execute_write(query, {"id": person_id})
	deleted = res[0].get("deleted") if res else False
	if not deleted:
		raise HTTPException(status_code=404, detail="Person not found")
	return {"deleted": True}


# ---------------------- Companies CRUD ----------------------


@api.post("/companies")
def create_company(payload: CompanyCreate):
	company_id = str(uuid.uuid4())
	query = "CREATE (c:Company {id:$id, name:$name, industry:$industry}) RETURN properties(c) AS company"
	params = {"id": company_id, "name": payload.name, "industry": payload.industry}
	res = db.execute_write(query, params)
	return res[0].get("company") if res else None


@api.get("/companies/{company_id}")
def get_company(company_id: str):
	query = "MATCH (c:Company {id:$id}) RETURN properties(c) AS company LIMIT 1"
	res = db.execute_read(query, {"id": company_id})
	if not res:
		raise HTTPException(status_code=404, detail="Company not found")
	return res[0].get("company")


@api.get("/companies")
def list_companies():
	query = "MATCH (c:Company) RETURN properties(c) AS company"
	res = db.execute_read(query)
	return [r.get("company") for r in res]


@api.put("/companies/{company_id}")
def update_company(company_id: str, payload: CompanyUpdate):
	props = {k: v for k, v in payload.dict().items() if v is not None}
	if not props:
		raise HTTPException(status_code=400, detail="No fields to update")
	query = "MATCH (c:Company {id:$id}) SET c += $props RETURN properties(c) AS company"
	res = db.execute_write(query, {"id": company_id, "props": props})
	if not res:
		raise HTTPException(status_code=404, detail="Company not found")
	return res[0].get("company")


@api.delete("/companies/{company_id}")
def delete_company(company_id: str):
	query = "OPTIONAL MATCH (c:Company {id:$id}) WITH c, c IS NOT NULL AS exists DETACH DELETE c RETURN exists AS deleted"
	res = db.execute_write(query, {"id": company_id})
	deleted = res[0].get("deleted") if res else False
	if not deleted:
		raise HTTPException(status_code=404, detail="Company not found")
	return {"deleted": True}


# ---------------------- Relationships ----------------------


@api.post("/relationships")
def create_relationship(payload: RelationshipCreate):
	query = """
	MATCH (a:Person {id:$person_id}), (b:Company {id:$company_id})
	MERGE (a)-[r:WORKS_AT]->(b)
	SET r.role = $role
	RETURN properties(r) AS relationship, properties(a) AS person, properties(b) AS company
	"""
	res = db.execute_write(query, {"person_id": payload.person_id, "company_id": payload.company_id, "role": payload.role})
	if not res:
		raise HTTPException(status_code=404, detail="Person or Company not found")
	return res[0]


@api.delete("/relationships")
def delete_relationship(payload: RelationshipCreate):
	query = "MATCH (a:Person {id:$person_id})-[r:WORKS_AT]->(b:Company {id:$company_id}) DELETE r RETURN true AS deleted"
	res = db.execute_write(query, {"person_id": payload.person_id, "company_id": payload.company_id})
	deleted = res and res[0].get("deleted")
	if not deleted:
		raise HTTPException(status_code=404, detail="Relationship not found")
	return {"deleted": True}
