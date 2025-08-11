import requests

token = "chave"
headers = {"Authorization": f"Bearer {token}"}
query = '{ viewer { login } }'

response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

print(response.status_code)
print(response.text)