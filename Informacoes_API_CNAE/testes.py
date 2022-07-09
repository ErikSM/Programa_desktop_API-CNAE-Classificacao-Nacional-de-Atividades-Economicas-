import json
import requests


def pula_linha():
    print("\n")

endereco_subclasses = "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses"
endereco_classes = "https://servicodados.ibge.gov.br/api/v2/cnae/classes"
endereco_divisoes = "https://servicodados.ibge.gov.br/api/v2/cnae/divisoes/"
endereco_grupos = "https://servicodados.ibge.gov.br/api/v2/cnae/grupos/"
endereco_sessoes = "https://servicodados.ibge.gov.br/api/v2/cnae/secoes"

request = requests.get(endereco_classes)
dicionario = json.loads(request.text)

print(dicionario[0])
pula_linha()
for i in dicionario[0]:
    print(i, ":", type(dicionario[0][i]))

pula_linha()

conjunto = set(dicionario[0])

print(conjunto)
pula_linha()
if 'grupo' in conjunto:
    print(dicionario[0]["grupo"]["descricao"])
else:
    print("nao pertence")

pula_linha()

