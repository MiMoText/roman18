# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import pandas as pd
import re
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def get_wikibase_result():
    endpoint_url = "https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql"

    query = """PREFIX wdt: <http://data.mimotext.uni-trier.de/prop/direct/>
    PREFIX wd: <http://data.mimotext.uni-trier.de/entity/>

    SELECT DISTINCT ?item ?count ?fullw where {
    FILTER(?count < 3)
    ?item wdt:P21 ?fullw.
    
    {

    SELECT ?item  (COUNT(?result) as ?count)
    WHERE {
    ?item wdt:P2 wd:Q2.
    ?item wdt:P21 ?fullworks.
    
    BIND(IF(CONTAINS(STR(?fullworks), "XML"), "XML",
            IF(CONTAINS(STR(?fullworks), "non_modernized"), "non_mod", 
            
            "txt file")) as ?result).
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

    }GROUP BY ?item 
    ORDER BY ?count
            }
    }"""


    def get_results(endpoint_url, query):
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()["results"]["bindings"]


    results = get_results(endpoint_url, query)

    result_df = pd.json_normalize(results)
    return result_df

def get_name(value, file_type):
    
    name = re.search(file_type.format("(.*?)"), value).group(0)
    name = name.split("/")[-1].split(".")[0]
    return name



def extract_filename(result_df, xml_string, files_non_mod_string, files_mod_string):

    result_df["filename"] = ""
    result_df["files_non_mod"] = ""
    result_df["files_mod"] = ""
    result_df["xml"] = ""

    df_new = pd.DataFrame(columns=["item.value", "name", "full_w"])
    print(df_new)

    for i, row in result_df.iterrows():

        if re.search(files_non_mod_string.format("(.*?)"), row["fullw.value"]):
            name = get_name(row["fullw.value"], files_non_mod_string)
            df_new.loc[len(df_new.index)] = [row["item.value"], name, xml_string.format(name)]
            df_new.loc[len(df_new.index)] = [row["item.value"], name, files_mod_string.format(name)]
        elif re.search(xml_string.format("(.*?)"), row["fullw.value"]):
            name = get_name(row["fullw.value"], xml_string)
            df_new.loc[len(df_new.index)] = [row["item.value"], name, files_non_mod_string.format(name)]
            df_new.loc[len(df_new.index)] = [row["item.value"], name, files_mod_string.format(name)]
        elif re.search(files_mod_string.format("(.*?)"), row["fullw.value"]):
            name = get_name(row["fullw.value"], files_mod_string)
            df_new.loc[len(df_new.index)] = [row["item.value"], name, xml_string.format(name)]
            df_new.loc[len(df_new.index)] = [row["item.value"], name, files_non_mod_string.format(name)]
        
    print(df_new)
    print(df_new.shape)
    df_new = df_new.drop_duplicates()
    print(df_new.shape)
    return df_new

def main():
    result_df = get_wikibase_result()
    result_df = result_df.drop(columns=["item.type", "count.type", "count.datatype", "fullw.type"])

    xml_string = "https://github.com/MiMoText/roman18/blob/master/XML-TEI/files/{}.xml"
    files_non_mod_string = "https://github.com/MiMoText/roman18/blob/master/plain/files_non_modernized/{}.txt"
    files_mod_string = "https://github.com/MiMoText/roman18/blob/master/plain/files/{}.txt"
    
    df_new = extract_filename(result_df, xml_string, files_non_mod_string, files_mod_string)

    with open("missing_full_works.csv", "w", encoding="utf8") as outfile:
        df_new.to_csv(outfile, sep=",", line_terminator="\n")
main()