import pandas as pd
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 10000)
from eurovoc_module.eurovoc_utils import create_eurovoc_sublabels



def sparql_res_df_grp_eurovocs(sparql_res):
	"""
	:param sparql_res: SPARQL query documents result as a pandas.DataFrame
	:return: dict
	"""
	rr2sorted = sparql_res.groupby("celex", group_keys=True).apply(lambda x: x).sort_values(by=['date'])
	rr2sorted_eurovoc_urls_grp_by_celex = rr2sorted["eurovoc"]
	rr2sorted_eurovoc_codes_grp_by_celex = rr2sorted_eurovoc_urls_grp_by_celex.apply(lambda x: x.split("/")[-1])
	eurovoc_map = {}
	for eurovoc_code in rr2sorted_eurovoc_codes_grp_by_celex.to_list():
		eurovoc_name = list(create_eurovoc_sublabels(eurovoc_code).keys())[0]
		eurovoc_map[eurovoc_code] = eurovoc_name
	return eurovoc_map




if __name__ == "__main__":
	from eurlex.src.eurlex import Eurlex

	eurlex_src = Eurlex()
	# Make a SPARQL query string to retrieve the latest 10 directives
	sparql_query = eurlex_src.make_query(resource_type="directive", order=True, limit=10,
										 include_date_force=True, include_date=True,
										 include_sector=True, include_eurovoc=True)
	# Retrieve the SPARQL query documents result as a pandas.DataFrame
	docs_res_df = eurlex_src.query_eurlex(sparql_query)
	
	eurovoc_map = sparql_res_df_grp_eurovocs(docs_res_df)
	
	eurovoc_map_inverted = {value: key for key, value in eurovoc_map.items()}
	
	sparql_res_df = docs_res_df.copy().groupby("celex", group_keys=True).apply(lambda x: x).sort_values(by=['date'])
	
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
