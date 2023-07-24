import pandas as pd
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 10000)
from eurovoc_module.eurovoc_utils import create_eurovoc_sublabels
from eurlex.src.eurlex import Eurlex



eur = Eurlex()

query = "PREFIX dcat: <http://www.w3.org/ns/dcat#>" \
		"PREFIX odp:  <http://data.europa.eu/euodp/ontologies/ec-odp#>" \
		"PREFIX dct: <http://purl.org/dc/terms/>" \
		"PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> " \
		"PREFIX foaf: <http://xmlns.com/foaf/0.1/> " \
		"SELECT " \
		"* " \
		"WHERE " \
		"{ " \
		"?d a dcat:Dataset " \
		"} " \
		"LIMIT 10"

# res1 = eur.query_eurlex(query)


# query2 = eur.make_query(resource_type="caselaw", order=True, limit=10)
# query2 = eur.make_query(resource_type="caselaw", order=True, limit=10, include_sector=True)
# query2 = eur.make_query(resource_type="caselaw", order=True, limit=10, include_sector=True, include_date=True)
# query2 = eur.make_query(resource_type="caselaw", order=True, limit=10, include_sector=True, include_date=True, include_date_force=True)
# query2 = eur.make_query(resource_type="caselaw", order=True, limit=1000, include_sector=True, include_date=True, include_date_force=True, include_eurovoc=True)
# query2 = eur.make_query(resource_type="any", order=True, limit=10, include_sector=True, include_date=True, include_date_force=True, include_eurovoc=True)
# query2 = eur.make_query(resource_type="directive", order=True, limit=100, include_sector=True, include_date=True, include_date_force=True, include_eurovoc=True)
# query2 = eur.make_query(resource_type="any", order=True, limit=10, include_sector=True, include_date=True, include_date_force=True, include_eurovoc=True)
query2 = eur.make_query(resource_type="directive", order=True, limit=10, include_sector=True, include_date=True, include_date_force=True, include_eurovoc=True)
res2 = eur.query_eurlex(query2)


# select distinct ?work ?type ?celex ?date ?dateforce ?eurovoc ?sector

# where{ ?work cdm:work_has_resource-type ?type.
# FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/DIR>||
# ?type=<http://publications.europa.eu/resource/authority/resource-type/DIR_IMPL>||
# ?type=<http://publications.europa.eu/resource/authority/resource-type/DIR_DEL>)
# FILTER not exists{?work cdm:work_has_resource-type <http://publications.europa.eu/resource/authority/resource-type/CORRIGENDUM>}


# OPTIONAL{?work cdm:work_is_about_concept_eurovoc ?eurovoc.
# graph ?gs    {
# 	?eurovoc skos:prefLabel ?subjectLabel
# 	filter (lang(?subjectLabel)="en") }.}
# OPTIONAL{?work cdm:resource_legal_id_sector ?sector.}
# FILTER not exists{?work cdm:do_not_index "true"^^<http://www.w3.org/2001/XMLSchema#boolean>}.}
# order by DESC(?date) limit 10
