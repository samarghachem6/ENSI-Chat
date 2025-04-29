from bs4 import BeautifulSoup
import requests
import json
import requests

url = "https://ensi.rnu.tn/fra/s1231/pages/299/Clubs-&-Associations"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
infos = soup.find_all('ul', class_="tick")
clubs = []
for info in infos:
    names = info.find_all("li")
    for li in names:
        clubs.append(li.get_text(strip=True))
        

club =[]
club.append({"question":"Quels sont les clubs disponibles à l'ENSI?",
             "answer": clubs})

with open("clubs.json", "w", encoding="utf-8") as f:
    json.dump(club, f, indent=2, ensure_ascii=False)


