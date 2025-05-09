import json
from ensi import ensi
from info_master import data_master
from matiereParFiliere import filiere
from doubleDiplome import dd
from vieAssociative import club
info = []
info.append({"question": "ou se trouve l'ENSI ?",
       "answer": "ENSI se trouve au Campus Universitaire de la Manouba."})

info.append({"question": "quelles sont les filières disponibles à l'ensi?",
       "answer": "Génie Logiciel, Intelligence Artificielle, Data Science for Computer Vision, Ingénierie pour la finance, IOT , Systèmes et logiciels embarqués."})

info.append({"question": "quels masters sont disponibles à l'ensi ?",
       "answer": "Iot et Data Science"})



data = ensi + data_master + filiere + dd + club + info
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

