import requests
import json
# Must install plotly: pip install plotly
from datetime import datetime

import pandas as pd
import plotly_express as px


# You may alternatively use matplotlib instead of plotly if desired

import urllib.parse
import os.path, hashlib
# For storing the results
import csv
year = 2022
month = 2

def request_cve_list(year, month):
   ''' Get CVE info from NIST using requests and return a json object '''
   web_address = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
   month_end_date = {1: '31', 2: '28', 3: '31', 4: '30', 5: '31', 6: '30', 7: '31', 8: '31', 9: '30', 10: '31', 11: '30', 12: '31'}
   params = {
        "resultsPerPage": 2000, "startIndex": 0, "pubStartDate":f"{year}-{month:02d}-01T00:00:00.000", "pubEndDate":f"{year}-{month:02d}-28T23:59:59.999"
   }
   headers = {
      "apiKey": "1da42625-031c-4517-bccd-f41b3351965c"
   }
   req1 = requests.get(url=web_address, params = params, headers = headers)
   print(req1.request.url)
   req = requests.get(req1.request.url+"&noRejected")
   print("req:", req)
   return req.json()

def write_CVEs_to_csv(year, month):
   ''' Task 1: write a CSV with key info in it '''
  
   filename = f"cve-{year}-{month:02d}.csv"
   if not os.path.isfile(filename):
       cve_json = request_cve_list(year, month)
       # Parse the JSON and write to CSV
       cve_list = cve_json["vulnerabilities"]
       with open(filename, 'w', newline='', encoding="utf-8") as file:
           writer = csv.writer(file)
           writer.writerow(["cveid", "publication date", "modification date",
            "exploitabilityScore", "impactScore", "vectorString", "attackVector", "attackComplexity",
            "privilegesRequired", "userInteraction", "scope", "confidentialityImpact", "integrityImpact",
            "availabilityImpact", "baseScore", "baseSeverity", "description"])
           for item in cve_list:
             if "cvssMetricV31" not in item["cve"]["metrics"]:
                 continue
             id = item["cve"]["id"]
             publication_date = item["cve"]["published"]
             modification_date =  item["cve"]["lastModified"]
             exploitability_score = item["cve"]["metrics"]["cvssMetricV31"][0]["exploitabilityScore"]
             impact_score = item["cve"]["metrics"]["cvssMetricV31"][0]["impactScore"]
             vector_string = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["vectorString"]
             attack_vector = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["attackVector"]
             attack_complexity = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["attackComplexity"]
             privileges_required = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["privilegesRequired"]
             user_interaction = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["userInteraction"]
             scope = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["scope"]
             confidentiality_impact = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["confidentialityImpact"]
             integrity_impact = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["integrityImpact"]
             availability_impact = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["availabilityImpact"]
             base_score = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
             base_severity = item["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
             description = item["cve"]["descriptions"]
             writer.writerow([id, publication_date, modification_date, exploitability_score, impact_score, vector_string, attack_vector, attack_complexity, privileges_required, user_interaction, scope, confidentiality_impact, integrity_impact, availability_impact, base_score, base_severity, description])
       print(f"The following file was created: {filename}")
       print(f"The following file was created: {filename}")
       print(f"The following file was created: {filename}")
       print(f"The following file was created: {filename}")

       print(f"The following file was created: {filename}")
   else:
       print(f"The following file already exists: {filename}")

def plot_CVEs(year,month,topnum=40):
   ''' Task 2: read that out and do a plot '''
   month = 2
   year = 2022
   filename = f"cve-{year}-{month:02d}.csv"
   df = pd.read_csv(filename)

   # Add baseScore values to score_list, sort in descending order, then grab first 40 values
   counter = 0
   top_40 = []
   score_list = []
   while counter < len(df):
         score_list.append(df.values[counter][3])
         counter+=1
   counter = 0
   score_list.sort(reverse=True)
   while counter < topnum:
       top_40.append(score_list[counter])
       counter+=1

   # Dump df then add values from top_40 list
   df = df.iloc[:40]
   df.index = top_40
   df['baseScore'] = top_40

   bar_plot = px.bar(df, x='cveid', y='baseScore', title="Highest-severity CVES for 2022-02", hover_name="description")
   bar_plot.update_xaxes(title_text="CVE")
   bar_plot.update_yaxes(title_text="Severity Score")
   bar_plot.write_image("bar.png")
   bar_plot.show()

   df = pd.read_csv(filename)
   scatter = px.scatter(df, x='baseScore', y='exploitabilityScore', title="CVE severity vs. exploitability for 2022-02", hover_name="description")
   scatter.update_xaxes(title_text="Severity Score")
   scatter.update_yaxes(title_text="Exploitability Score")
   scatter.write_image("scatter.png")
   scatter.show()


   
if __name__ =="__main__":
   # Do not modify
   year = 2022
   month = 2
   write_CVEs_to_csv(year, month)
   plot_CVEs(year, month)
   h = hashlib.new('sha1')
   h.update(open("cve-2022-02.csv").read().encode("utf-8"))
   print(h.hexdigest())