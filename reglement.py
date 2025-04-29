# from bs4 import BeautifulSoup
# import requests
# import csv

# url = "https://ensi.rnu.tn/fra/s1226/pages/443/Administration"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")

# pdf_links = soup.find_all("a", class_="downloadLink-blue-round")

# pdf_url = pdf_links[1]["href"]
    
# if pdf_url.startswith("/"):
#     pdf_url = "https://ensi.rnu.tn" + pdf_url

# scraped_text=pdf_url

# with open('scraped_data.csv', 'a', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Reglement interne :'])  
#     writer.writerow([scraped_text]) 