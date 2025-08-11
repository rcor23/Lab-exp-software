import requests

token = "chave"
print(f"Token length: {len(token)}")
print(f"Token (repr): {repr(token)}")

headers = {"Authorization": f"Bearer {token}"}
query = '{ viewer { login } }'

response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

print("Status:", response.status_code)
print("Resposta da API:")
print(response.text)
