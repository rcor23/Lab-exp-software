import requests
import json

TOKEN = "chave"
url = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Python Script"
}

def buscar_repositorios(qtd_total=100, por_pagina=10):
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
                  name
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

        response = requests.post(url, json={'query': query}, headers=headers)
        data = response.json()

        search_data = data["data"]["search"]
        repositorios.extend(search_data["edges"])

        print(f"Página {pagina} - Repositórios coletados até agora: {len(repositorios)}")

        cursor = search_data["pageInfo"]["endCursor"]
        if not search_data["pageInfo"]["hasNextPage"]:
            break

        pagina += 1

    return repositorios[:qtd_total]

repos = buscar_repositorios(100, 10)

with open("lab01_data.json", "w", encoding="utf-8") as f:
    json.dump(repos, f, indent=4, ensure_ascii=False)
