import json
import re
import xmltodict, json
import requests
import json


# EUROVOCS = {1193:"group of companies", 1496:"public investment", 1313:"direct tax"}


# def eurovoc_id_2_name(eurovoc_id:int) -> str:

# label_id = "100148"

# headers = {"charset": "utf-8", "Content-Type": "application/json"}
# url = "https://publications.europa.eu/resource/authority/eurovoc/100199"
# url = f"https://publications.europa.eu/resource/authority/eurovoc/{label_id}"
# res = requests.get(url, headers=headers)
# r = res
# c = r.content
# result = json.loads(c)

# o = xmltodict.parse(res.text)
# j = json.dumps(o) # '{"e": {"a": ["text", "text"]}}'


# l = json.loads(j)["rdf:RDF"]['rdf:Description']
# print(l)
# print("\n")
# print(json.loads(j)["rdf:RDF"]['rdf:Description'][0])


def eurovoc_xmlrdf_response_2_label(xmlrdf_response):
	o = xmltodict.parse(xmlrdf_response.text)
	j = json.dumps(o)
	labels = [i["skos:prefLabel"] for i in json.loads(j)["rdf:RDF"]['rdf:Description'] if "skos:prefLabel" in list(i.keys())][0]
	# lang_label =
	for label in labels:
		if "@xml:lang" in list(label.keys()) and label["@xml:lang"] == "en":
			# return True
			# return label["#text"]
			return re.sub('[^a-zA-Z]+ ', '', label["#text"])



# def eurovoc_xmlrdf_response_description_filter(xmlrdf_response, tag):
# 	label = xmlrdf_response.url.split("/")[-1]
# 	o = xmltodict.parse(res.text)
# 	j = json.dumps(o)
# 	labels = [i[tag] for i in json.loads(j)["rdf:RDF"]['rdf:Description'] if i[tag].split("/")[-1] != label]

def extract_eurovoc_xmlrdf_response_sublabels(xmlrdf_response, return_urls=False):
	label = xmlrdf_response.url.split("/")[-1]
	o = xmltodict.parse(xmlrdf_response.text)
	j = json.dumps(o)
	sublabel_urls = [i['@rdf:about'] for i in json.loads(j)["rdf:RDF"]['rdf:Description'] if i['@rdf:about'].split("/")[-1] != label]
	if return_urls is False:
		eurovoc_sublabel_codes = [sublabel.split("/")[-1] for sublabel in sublabel_urls if sublabel.split("/")[-1].isnumeric()]
		return eurovoc_sublabel_codes
	else:
		eurovoc_sublabel_urls = [sublabel for sublabel in sublabel_urls if sublabel.split("/")[-1].isnumeric()]
		return eurovoc_sublabel_urls

# print(eurovoc_xmlrdf_response_2_label(res))
# print(extract_eurovoc_xmlrdf_response_sublabels(res))

# headers = {"charset": "utf-8", "Content-Type": "application/json"}
# for sublabel_url in extract_eurovoc_xmlrdf_response_sublabels(res, return_urls=True):
# 	sublabel_eurovoc_xmlrdf_res = requests.get(sublabel_url, headers=headers)
# 	sublabel_eurovoc_name = eurovoc_xmlrdf_response_2_label(sublabel_eurovoc_xmlrdf_res)
# 	print(f"sublabel_url: {sublabel_url} | sublabel_eurovoc_name: {sublabel_eurovoc_name}")



def create_eurovoc_sublabels(label_id="100148"):
	headers = {"charset": "utf-8", "Content-Type": "application/json"}
	url = f"https://publications.europa.eu/resource/authority/eurovoc/{label_id}"
	res = requests.get(url, headers=headers)
	label_eurovoc_name = eurovoc_xmlrdf_response_2_label(res).lower()
	# eurovoc_sublabels_dir = {label_eurovoc_name:{}}
	eurovoc_sublabels_dir = {label_eurovoc_name:{}}
	for sublabel_url in extract_eurovoc_xmlrdf_response_sublabels(res, return_urls=True):
		sublabel_eurovoc_xmlrdf_res = requests.get(sublabel_url, headers=headers)
		sublabel_eurovoc_code = sublabel_eurovoc_xmlrdf_res.url.split("/")[-1]
		sublabel_eurovoc_name = eurovoc_xmlrdf_response_2_label(sublabel_eurovoc_xmlrdf_res)
		eurovoc_sublabels_dir[label_eurovoc_name].update({sublabel_eurovoc_name: sublabel_eurovoc_code})
	return eurovoc_sublabels_dir


if __name__ == "__main__":
	
	# politics = 100142
	# international relations = 100143
	# european union = 100144
	# law = 100145
	# economics = 100146
	# trade = 100193
	# finance = 100148
	# social questions = 100149
	# education and communications = 100150
	# science = 100151
	# business and competition = 100152
	# employment and working conditions = 100153
	# transport = 100154
	# environment = 100155
	# agriculture, forestry and fisheries = 100156
	# agri-foodstuffs = 100157
	# production, technology and research = 100158
	# energy = 100159
	# industry = 100160
	# geography = 100161
	# international organisations = 100162
	
	fin = create_eurovoc_sublabels(label_id="100148")
	print("\n")
	print("\n")
	print(fin)
	# http://eurovoc.europa.eu/1193
	fin2 = create_eurovoc_sublabels(label_id="1193")
	print("\n")
	print("\n")
	print(fin2)
