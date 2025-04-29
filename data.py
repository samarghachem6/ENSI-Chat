import json
from ensi import ensi
from info_master import data_master
from matiereParFiliere import filiere
from doubleDiplome import dd
from vieAssociative import club


data = ensi + data_master + filiere + dd + club
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

