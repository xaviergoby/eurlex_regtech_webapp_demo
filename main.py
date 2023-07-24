import time
import data_src
# from data_src import DataSrc
# from sparql_query_builder import SparqlQueryBuilder
from src_utils import get_sparql_query_results
import streamlit as st


# sparl_query_builder = SparqlQueryBuilder()
# query = sparl_query_builder.build_query()

# eurlex_src = DataSrc(base_sparql_query_name="eurlex_base_financial_domain_sparql_query")
# eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_sparql_2019-01-07_V2")
eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_eurlex_sparql_query")
query = eurlex_src.query_str
# results = get_sparql_query_results(query)

updated_query = ''

st.title("EurLex SPARQL Publications Retrieval Demo")

# descriptor_term = st.text_input("Sparql queries file name")
# FILTER( ?date = "2014-01-01"^^xsd:date)
init_pub_date = st.text_input("Please enter a starting date for publications desired (YYYY-MM-DD)")

updated_query = query.replace('FILTER( ?date > "2014-01-01"^^xsd:date)', f'FILTER( ?date > "{init_pub_date}"^^xsd:date)')

while updated_query == '':
	time.sleep(1)
	
res_limit = None

res_limit = st.text_input("Please enter a limit number of results desired")

updated_query = query.replace('LIMIT 10', f'LIMIT {res_limit}')

while res_limit is None:
	time.sleep(1)

results = get_sparql_query_results(updated_query)
for i, res in enumerate(results["results"]["bindings"], start=1):
	print(f"\n~~~~~~~~~~~ doc_url KEYS: {res.keys()} ~~~~~~~~~~~")
	print(f"~~~~~~~~~~~ doc_url VALUES: {res.values()} ~~~~~~~~~~~")
	doc_url = res["cellarURIs"]["value"]
	doc_date = res["workDates"]["value"]
	doc_title = res["workTitles"]["value"]
	doc_subjects = res["subjects"]["value"]
	doc_celex_id = res["celexIds"]["value"]
	# doc_ids = res["workIds"]["value"]
	st.write(f"**Document # {i}:**")
	st.write(f"URL: {doc_url}")
	st.write(f"Date: {doc_date}")
	st.write(f"Title: {doc_title}")
	st.write(f"Subjects: {doc_subjects}")
	st.write(f"CELEX: {doc_celex_id}")
	# st.write(f"IDs: {doc_ids}")
	# print(f"||||||||||| IDs: {doc_ids}")
	st.write("---")

