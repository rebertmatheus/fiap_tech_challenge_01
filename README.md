VITINIGPT - API de Dados da Vitivinicultura Gaúcha
PythonPython](

FastAPIFastAPI](https://fastapi.

API para acesso aos dados estatísticos da produção, comercialização e processamento de uvas, vinhos e derivados do estado do Rio Grande do Sul.

📋 Sobre o Projeto
O VITINIGPT oferece uma interface moderna para acessar dados estatísticos do setor vitivinícola do Rio Grande do Sul. A API permite consultar informações sobre:

Produção de uvas e vinhos
Processamento por tipos de uva (Viníferas, Americanas e Híbridas, Uvas de Mesa)
Comercialização de produtos derivados da uva
Importação e Exportação de vinhos e derivados
Os dados são organizados por ano e segmentados em diferentes categorias, oferecendo uma visão completa do setor.

🚀 Instalação
Pré-requisitos
Python 3.8+
pip
Passos para Instalação
Clone o repositório:
bash
Copiar

   git clone https://github.com/rebertmatheus/fiap_tech_challenge_01.git
   cd fiap_tech_challenge_01
Crie e ative um ambiente virtual:
bash
Copiar

   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No Linux/macOS
   source venv/bin/activate
Instale as dependências:
bash
Copiar

   pip install -r requirements.txt

🏃‍♂️ Executando o Projeto
Para executar o servidor:

bash
Copiar

python -m tech_challenge
O servidor estará disponível em http://localhost:8001

🔑 Autenticação
A API utiliza autenticação via token JWT. Para obter um token:

bash
Copiar

curl -X POST "http://localhost:8001/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario&password=senha"
O token deve ser incluído nos headers de todas as requisições:

bash
Copiar

curl "http://localhost:8001/products/PRODUCTION" \
  -H "Authorization: Bearer seu_token_aqui"
📚 Endpoints da API
Documentação Interativa
Swagger UI: http://localhost:8001/docs
ReDoc: http://localhost:8001/redoc
Principais Endpoints
1. Obter dados por segmento
GET /products/{segment}

Parâmetros:

segment: PRODUCTION, PROCESSING, SALES, IMPORTATION, EXPORTATION
year (opcional): Ano desejado, se omitido retorna o último ano disponível
sub_option (opcional): Subcategoria específica dentro do segmento
Exemplos:

GET /products/PRODUCTION

GET /products/PROCESSING?year=2022

GET /products/IMPORTATION?suboption=TABLEWINE

2. Obter opções de subcategorias disponíveis
GET /segments/{segment}/options

Exemplo:

GET /segments/PROCESSING/options

3. Obter anos disponíveis para um segmento
GET /segments/{segment}/years

Exemplo:

GET /segments/PRODUCTION/years

📊 Estrutura de Dados
Os dados são retornados no formato JSON seguindo esta estrutura:

json
Copiar

[
  {
    "name": "Nome da categoria",
    "quantity": 1234567,
    "unit": "unidade",
    "group": "",
    "amount": 12345.67,
    "sub_products": [
      {
        "name": "Nome do produto",
        "quantity": 123456,
        "unit": "kg",
        "group": "Nome da categoria",
        "amount": 1234.56
      }
    ]
  }
]
Onde:

name: Nome da categoria ou produto
quantity: Quantidade ou volume
unit: Unidade de medida (kg, L, etc.)
group: Grupo ao qual o produto pertence
amount: Valor monetário (quando disponível)
sub_products: Lista de produtos dentro de uma categoria
🔍 Subcategorias Disponíveis
Importação/Exportação
TABLE_WINE (vinho de mesa)
SPARKLING_WINE (espumante)
FRESH_GRAPES (uvas frescas)
RAISINS (uvas passas)
GRAPE_JUICE (suco de uva)
Processamento
VINIFERA (Viníferas)
AMERICAN_HYBRID (Americanas e Híbridas)
TABLE_GRAPE (Uvas de Mesa)
UNCLASSIFIED (Sem classificação)

🤝 Contribuição
Contribuições são bem-vindas! Por favor, siga estes passos:

Fork o projeto
Crie sua branch de feature (git checkout -b feature/nova-feature)
Commit suas mudanças (git commit -am 'Adiciona nova feature')
Push para a branch (git push origin feature/nova-feature)
Crie um Pull Request
📄 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

