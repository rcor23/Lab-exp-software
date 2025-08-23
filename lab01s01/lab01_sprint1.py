import requests
import json
import pandas as pd
import time


TOKEN = "sya"  
url = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Python Script"
}


def buscar_repositorios(qtd_total=1000, por_pagina=20, max_retries=3):
    repositorios = []
    cursor = None
    pagina = 1

    while len(repositorios) < qtd_total:
        query = f"""
        {{
          search(query: "stars:>0 sort:stars-desc", type: REPOSITORY, first: {por_pagina}, after: {json.dumps(cursor) if cursor else "null"}) {{
            pageInfo {{
              endCursor
              hasNextPage
            }}
            edges {{
              node {{
                ... on Repository {{
                  nameWithOwner
                  url
                  createdAt
                  primaryLanguage {{
                    name
                  }}
                  pullRequests(states: MERGED) {{
                    totalCount
                  }}
                  releases {{
                    totalCount
                  }}
                  updatedAt
                  issues {{
                    totalCount
                  }}
                  closedIssues: issues(states: CLOSED) {{
                    totalCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        for attempt in range(1, max_retries + 1):
            response = requests.post(url, json={'query': query}, headers=headers)
            print(f"\n--- Página {pagina} --- Attempt {attempt} --- Status code: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                except Exception:
                    print("⚠️ Resposta não é JSON. Conteúdo bruto:")
                    print(response.text[:500])
                    break
                break
            else:
                print(f"⚠️ Erro {response.status_code}. Tentando novamente em 5s...")
                time.sleep(5)
        else:
            print("⚠️ Falha após múltiplas tentativas. Abortando.")
            break

        if "errors" in data:
            print("⚠️ Erro na requisição:", json.dumps(data["errors"], indent=2))
            break

        search_data = data.get("data", {}).get("search")
        if not search_data:
            print("⚠️ Não foi possível acessar 'data.search'. Resposta recebida:")
            print(json.dumps(data, indent=2))
            break

        repositorios.extend(search_data["edges"])
        print(f"Repositórios coletados até agora: {len(repositorios)}")

        cursor = search_data["pageInfo"]["endCursor"]
        if not search_data["pageInfo"]["hasNextPage"]:
            break

        pagina += 1

    return repositorios[:qtd_total]


print("🔎 Coletando dados dos repositórios...")
repos = buscar_repositorios(1000, 20)  


dados = []
for repo in repos:
    node = repo["node"]
    dados.append({
        "nameWithOwner": node["nameWithOwner"],
        "url": node["url"],
        "createdAt": node["createdAt"],
        "primaryLanguage": node["primaryLanguage"]["name"] if node["primaryLanguage"] else None,
        "mergedPullRequests": node["pullRequests"]["totalCount"],
        "releases": node["releases"]["totalCount"],
        "updatedAt": node["updatedAt"],
        "issues": node["issues"]["totalCount"],
        "closedIssues": node["closedIssues"]["totalCount"],
    })


if dados:
    df = pd.DataFrame(dados)
    df.to_csv("lab01_data.csv", index=False, encoding="utf-8")
    print("\n✅ Coleta finalizada! Dados salvos em lab01_data.csv com", len(df), "repositórios.")
else:
    print("\n⚠️ Nenhum dado coletado. Verifique o erro acima.")
