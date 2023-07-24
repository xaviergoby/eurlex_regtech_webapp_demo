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

# url = "http://publications.europa.eu/resource/celex/32016R0679"
# data1 = eur.get_data(url, data_type="text")


print(res2)
print("\n")
# print(res2.loc[0])
for idx in res2.index.to_list():
	print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ idx ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	for col_i_title in res2.loc[idx].index.to_list():
		print(f"{col_i_title}: {res2.loc[idx][col_i_title]}")



# rr2sorted = res2.groupby("celex", group_keys=True).apply(lambda x: x).sort_values(by=['date'])

# rr2sorted_eurovoc_urls_grp_by_celex = rr2sorted["eurovoc"]
# rr2sorted_eurovoc_codes_grp_by_celex = rr2sorted_eurovoc_urls_grp_by_celex.apply(lambda x: x.split("/")[-1])


def sparql_res_df_grp_eurovocs(sparql_res):
	rr2sorted = sparql_res.groupby("celex", group_keys=True).apply(lambda x: x).sort_values(by=['date'])
	rr2sorted_eurovoc_urls_grp_by_celex = rr2sorted["eurovoc"]
	rr2sorted_eurovoc_codes_grp_by_celex = rr2sorted_eurovoc_urls_grp_by_celex.apply(lambda x: x.split("/")[-1])
	eurovoc_map = {}
	for eurovoc_code in rr2sorted_eurovoc_codes_grp_by_celex.to_list():
		eurovoc_name = list(create_eurovoc_sublabels(eurovoc_code).keys())[0]
		eurovoc_map[eurovoc_code] = eurovoc_name
	return eurovoc_map
	
eurovoc_map = sparql_res_df_grp_eurovocs(res2)
eurovoc_map_inverted = {value: key for key, value in eurovoc_map.items()}



sparql_res_df = res2.copy().groupby("celex", group_keys=True).apply(lambda x: x).sort_values(by=['date'])

for idx, row in sparql_res_df.iterrows():
	print(f"row:{row}")
	grp_eurovoc_names_map = map(lambda x: eurovoc_map[x], sparql_res_df.loc[idx[0]]["eurovoc"].apply(lambda x: x.split("/")[-1]).to_list())
	# grp_eurovoc_names_map = map(lambda x: sparql_res_df.loc[idx[0]]["eurovoc"].apply(lambda x: x.split("/")[-1]).to_list(), eurovoc_map[x])
	grp_eurovoc_names = list(grp_eurovoc_names_map)
	print(f"grp_eurovoc_names:{grp_eurovoc_names}")
	print(f"idx[0]:{idx[0]}")
	# row["eurovoc"] = grp_eurovoc_names
	# sparql_res_df.loc[idx[0], "eurovoc"] = grp_eurovoc_names
	sparql_res_df.loc[idx[0], "eurovoc_name"] = grp_eurovoc_names
	
print(f"\nsparql_res_df:\n{sparql_res_df}")
	
	
