from pydantic import BaseModel
from typing import Optional


class PersonCreate(BaseModel):
	name: str
	age: Optional[int]
	email: Optional[str]


class PersonUpdate(BaseModel):
	name: Optional[str]
	age: Optional[int]
	email: Optional[str]


class CompanyCreate(BaseModel):
	name: str
	industry: Optional[str]


class CompanyUpdate(BaseModel):
	name: Optional[str]
	industry: Optional[str]


class RelationshipCreate(BaseModel):
	person_id: str
	company_id: str
	role: Optional[str]

