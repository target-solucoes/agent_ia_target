"""
Arquivo para testar diferentes tipos de queries com o agente
"""
from duckdb_agent import agent

def test_basic_queries():
    """Testa queries básicas sobre o dataset"""
    queries = [
        "Quantas linhas e colunas tem o dataset?",
        "Quais são os nomes de todas as colunas?",
        "Mostre um resumo estatístico dos dados numéricos",
        "Quais são os tipos de dados de cada coluna?",
        "Mostre as primeiras 5 linhas do dataset",
    ]
    
    print("=== TESTANDO QUERIES BASICAS ===\n")
    
    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 50)
        try:
            agent.print_response(query)
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            print("\n" + "="*80 + "\n")

def test_analytical_queries():
    """Testa queries analíticas mais complexas"""
    queries = [
        "Identifique valores nulos ou missing em cada coluna",
        "Mostre a distribuição de valores únicos nas colunas categóricas",
        "Calcule correlações entre variáveis numéricas",
        "Identifique outliers nos dados numéricos",
        "Faça um agrupamento por uma coluna categórica principal",
    ]
    
    print("=== TESTANDO QUERIES ANALITICAS ===\n")
    
    for i, query in enumerate(queries, 1):
        print(f"Query Analitica {i}: {query}")
        print("-" * 50)
        try:
            agent.print_response(query)
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            print("\n" + "="*80 + "\n")

def test_sql_queries():
    """Testa queries SQL diretas com DuckDB"""
    sql_queries = [
        "SELECT COUNT(*) as total_linhas FROM dados_comerciais;",
        "SELECT * FROM dados_comerciais LIMIT 3;",
        "DESCRIBE dados_comerciais;",
        "SELECT COUNT(*) as total_colunas FROM information_schema.columns WHERE table_name = 'dados_comerciais';",
    ]
    
    print("=== TESTANDO QUERIES SQL ===\n")
    
    for i, query in enumerate(sql_queries, 1):
        print(f"SQL Query {i}: {query}")
        print("-" * 50)
        try:
            agent.print_response(f"Execute esta query SQL: {query}")
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"Erro ao executar SQL query: {e}")
            print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    print("Iniciando testes de queries do agente...\n")
    
    # Executar todos os tipos de teste
    test_basic_queries()
    test_analytical_queries()
    test_sql_queries()
    
    print("Testes concluídos!")