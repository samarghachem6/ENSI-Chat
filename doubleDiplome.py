from bs4 import BeautifulSoup
import requests
import json

response = requests.get('https://ensi.rnu.tn/fra/s1270/pages/450/Double-dipl%C3%B4me')
soup = BeautifulSoup(response.text,'html.parser')
info=soup.find_all('li',style="text-align: justify;")
divs=soup.find('div',class_ ='content').find_all('div')



dd=[]
items =[li.get_text(strip=True) for li in info]
dd.append({"question": "In which French universities does ENSI offer double degrees ?",
           "answer": " , ".join(li.get_text(strip=True) for li in info)})

dd.append({"question" : "In which German universities does ENSI offer double degrees?",
           "answer": divs[3].get_text(strip=True) +" , " +  divs[4].get_text(strip=True)})

dd.append({"question" : "In which Canadian universities does ENSI offer double degrees?",
           "answer": divs[6].get_text(strip=True)})
dd.append( {
    "question": "what double degrees does ENSI offer?",
    "answer": "ENSI offers double degree opportunities in multiple countries, France, Germany and Canada"
  })

with open("dd.json", "w", encoding="utf-8") as f:
    json.dump(dd, f, indent=2, ensure_ascii=False)


