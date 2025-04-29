import requests
from bs4 import BeautifulSoup
import json

url = "https://ensi.rnu.tn/fra/s1226/pages/260/Découvrir-l'ENSI"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

divs = soup.find_all("div", style="text-align: justify;")
#print(divs[2].get_text(strip=True))

ensi = []
ensi.append({
    "question": "Idée générale sur l'ENSI",
    "answer": divs[2].get_text(strip=True)})

# Save to JSON
with open("ensi.json", "w", encoding="utf-8") as f:
    json.dump(ensi, f, indent=2, ensure_ascii=False)



