from dataclasses import dataclass




@dataclass
class SparqlPubQueryRes:
	"""
	Dataclass/model of a single publication from a SPARQL query result set.
	"""
	temp_id: int
	celex: str
	publication_date: str
	title: str
	language: str
	authors: list[str]
	subjects: list[str]
	
