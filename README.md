# Projeto: Coleta de Repositórios Populares do GitHub (GraphQL API)

Este projeto utiliza a API GraphQL do GitHub para buscar informações sobre os repositórios mais populares, salvando os dados em um arquivo `lab01_data.json`.

---

## Pré-requisitos

Antes de rodar o projeto, você precisa ter:

1. **Python 3.8 ou superior**  
   Baixe em: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
   Durante a instalação, marque a opção **"Add Python to PATH"**.

2. **Conta no GitHub** e **Token de acesso pessoal** (Personal Access Token).  
   - Crie o token em: [https://github.com/settings/tokens](https://github.com/settings/tokens)  
   - Dê permissões de leitura para *public_repo*.
   - Copie e substitua no código na variável `TOKEN`.

3. **Biblioteca requests** instalada:
   ```bash
   pip install requests
