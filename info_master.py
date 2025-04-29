import requests
from bs4 import BeautifulSoup
import urllib.parse 
import json
import pdfplumber

url = "https://ensi.rnu.tn/fra/s1270/pages/441/Master-de-recherche-en-Sciences-de-l-Informatique"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
info = soup.find_all("li",style="text-align: justify;")
div = soup.find("div", class_="content").find("div")


#Plan d'études M1, M2_ds, M2_iot

def get_pdf_links(url, indices):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = [a["href"] for a in soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))]

    def build_url(href):
        decoded_href = urllib.parse.unquote(href)  # Remove incorrect encoding
        full_url = decoded_href if decoded_href.startswith("http") else urllib.parse.urljoin(url, decoded_href)
        return urllib.parse.quote(full_url, safe=":/")  # Re-encode correctly

    return [build_url(pdf_links[i]) for i in indices]

url = "https://ensi.rnu.tn/fra/s1270/pages/509/Mersi"
pdf_url_m1, pdf_url_ds, pdf_url_iot = get_pdf_links(url, [4, 6, 8])


data_master = []
def subjects_extraction(pdf_path, page_num, col=1):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        table = page.extract_table()
        column = [row[col] for row in table[1:]]
        return [item.replace("\n", " ").strip() for item in column if item]

#Matières M1
pdf_response = requests.get(pdf_url_m1)
with open("plan_m1.pdf", "wb") as f:
    f.write(pdf_response.content)
M1_S1 = ", ".join(subjects_extraction("plan_m1.pdf",0))
M1_S2 = ", ".join(subjects_extraction("plan_m1.pdf",1))

def group_fragments(lines):
    grouped = []
    buffer = ""
    for line in lines:
        if line.startswith("UO1"):  
            break
        if line.startswith("UF"):
            if buffer:
                grouped.append(buffer.strip())
            buffer = line
        else:
            buffer += " " + line
    if buffer:
        grouped.append(buffer.strip())
    return grouped


#Matières M2 DS
pdf_response_ds = requests.get(pdf_url_ds)
with open("plan_m2_ds.pdf", "wb") as f:
    f.write(pdf_response_ds.content)
M2_ds = ", ".join(group_fragments(subjects_extraction("plan_m2_ds.pdf",0)))


#Matières M2 IOT
pdf_response_iot = requests.get(pdf_url_iot)
with open("plan_m2_iot.pdf", "wb") as f:
    f.write(pdf_response_iot.content)
M2_iot = " , ".join(subjects_extraction("plan_m2_iot.pdf",0))

data_master.append({
    "question": "Informations sur le Master en sciences de l'informatique?",
    "answer": div.get_text(strip=True) +  info[0].get_text(strip=True) + info[1].get_text(strip=True)
})

data_master.append({
    "question": "Quelles sont les matières du master M1 ?",
    "answer": M1_S1 +', ' + M1_S2
})

data_master.append({
    "question": "Quelles sont les matières du master M2 DS ?",
    "answer": M2_ds
})

data_master.append({
    "question": "Quelles sont les matières du master M2 IOT ?",
    "answer": M2_iot
})


data_master.append({
    "question": "Plan d'études M1",
    "answer": f"Plan M1: {pdf_url_m1}"
})

data_master.append({
    "question": "Plan d'études M2 DS?",
    "answer": f"=Plan M2 DS: {pdf_url_ds}"
})

data_master.append({
    "question": "Plan d'études M2 IOT?",
    "answer": f"Plan M2 IOT: {pdf_url_iot}"
})

# Save to JSON
with open("data_master.json", "w", encoding="utf-8") as f:
    json.dump(data_master, f, indent=2, ensure_ascii=False)






