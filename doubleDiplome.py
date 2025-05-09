from bs4 import BeautifulSoup
import requests
import json

response = requests.get('https://ensi.rnu.tn/fra/s1270/pages/450/Double-dipl%C3%B4me')
soup = BeautifulSoup(response.text,'html.parser')
info=soup.find_all('li',style="text-align: justify;")
divs=soup.find('div',class_ ='content').find_all('div')



dd=[]
items =[li.get_text(strip=True) for li in info]
dd.append({"question": "Dans quelles universités françaises l'ENSI propose-t-elle des doubles diplômes ?",
           "answer": " , ".join(li.get_text(strip=True) for li in info)})

dd.append({"question" : "Dans quelles universités allemandes l'ENSI propose-t-elle des doubles diplômes ?",
           "answer": divs[3].get_text(strip=True) +" , " +  divs[4].get_text(strip=True)})

dd.append({"question" : "Dans quelles universités canadiennes l'ENSI propose-t-elle des doubles diplômes ?",
           "answer": divs[6].get_text(strip=True)})
dd.append( {
    "question": "Quels sont les doubles diplômes proposés par l'ENSI ?",
    "answer": "L'ENSI offre des possibilités de double diplôme dans plusieurs pays, en France, en Allemagne et au Canada."
  })

with open("dd.json", "w", encoding="utf-8") as f:
    json.dump(dd, f, indent=2, ensure_ascii=False)


