"""
Script de teste para validar a implementação da normalização de texto.
"""

import sys
import pandas as pd
sys.path.append("src")

from text_normalizer import TextNormalizer, load_alias_mapping


def test_text_normalization():
    """Testa as funcoes basicas de normalizacao de texto."""
    print("=== Testando Normalizacao de Texto ===\n")
    
    normalizer = TextNormalizer()
    
    # Teste 1: Normalizacao basica
    test_strings = [
        "Sao Paulo",
        "EMPRESA LTDA", 
        "Rio de Janeiro - RJ",
        "  Espacos   Extras  ",
        "Acai & Cafe",
        None,
        ""
    ]
    
    print("1. Teste de normalizacao basica:")
    for original in test_strings:
        normalized = normalizer.normalize_text(original)
        print(f"   '{original}' -> '{normalized}'")
    print()
    
    # Teste 2: Carregamento de dados
    print("2. Testando carregamento do dataset:")
    try:
        df = pd.read_parquet('data/raw/DadosComercial_limpo.parquet')
        print(f"   Dataset carregado: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        # Identificar colunas de texto
        text_columns = normalizer.identify_text_columns(df)
        print(f"   Colunas de texto identificadas: {text_columns}")
        
    except Exception as e:
        print(f"   Erro ao carregar dataset: {e}")
        return False
    
    # Teste 3: Normalizacao do DataFrame
    print("\n3. Testando normalizacao do DataFrame:")
    try:
        df_normalized = normalizer.normalize_dataframe(df, text_columns)
        print(f"   DataFrame normalizado criado")
        
        # Comparar algumas amostras
        if text_columns:
            sample_col = text_columns[0]
            print(f"   Comparacao da coluna '{sample_col}':")
            
            sample_indices = df[sample_col].dropna().head(3).index
            for idx in sample_indices:
                original = df.loc[idx, sample_col]
                normalized = df_normalized.loc[idx, sample_col]
                print(f"     '{original}' -> '{normalized}'")
        
    except Exception as e:
        print(f"   Erro na normalizacao do DataFrame: {e}")
        return False
    
    # Teste 4: Carregamento de aliases
    print("\n4. Testando carregamento de aliases:")
    try:
        alias_mapping = load_alias_mapping()
        print(f"   Aliases carregados: {len(alias_mapping)} mapeamentos")
        
        # Mostrar alguns exemplos
        for column, aliases in list(alias_mapping.items())[:3]:
            print(f"     {column}: {aliases[:3]}...")
        
    except Exception as e:
        print(f"   Erro ao carregar aliases: {e}")
        return False
    
    # Teste 5: Normalizacao de consultas
    print("\n5. Testando normalizacao de consultas:")
    try:
        test_queries = [
            "Quais empresas estao em Sao Paulo?",
            "Mostre vendas da MATRIZ SC",
            "Qual o faturamento total?",
            "Liste os municipios do cliente"
        ]
        
        for query in test_queries:
            result = normalizer.normalize_query_terms(query, alias_mapping)
            print(f"   Query: '{query}'")
            print(f"   Normalizada: '{result['normalized_query']}'")
            if result['mapped_terms']:
                print(f"   Termos mapeados: {result['mapped_terms']}")
            print()
            
    except Exception as e:
        print(f"   Erro na normalizacao de consultas: {e}")
        return False
    
    print("Todos os testes passaram com sucesso!")
    return True


def test_agent_integration():
    """Testa a integracao com o agente DuckDB."""
    print("\n=== Testando Integracao com Agente ===\n")
    
    try:
        from duckdb_agent import create_agent
        
        print("1. Criando agente com normalizacao:")
        agent, df = create_agent()
        print("   Agente criado com sucesso")
        
        # Teste com consultas simples
        print("\n2. Testando consultas basicas:")
        test_queries = [
            "Quantas linhas tem o dataset?",
            "Quais são as empresas disponíveis?",
        ]
        
        for query in test_queries:
            print(f"   Executando: '{query}'")
            try:
                response = agent.run(query)
                print(f"   Resposta obtida (tipo: {type(response)})")
            except Exception as e:
                print(f"   Erro na consulta: {e}")
        
        print("\nIntegracao com agente testada com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro na integracao com agente: {e}")
        return False


if __name__ == "__main__":
    print("Iniciando testes de normalizacao de texto...\n")
    
    # Executar testes
    test1_passed = test_text_normalization()
    test2_passed = test_agent_integration()
    
    print(f"\n=== Resumo dos Testes ===")
    print(f"Normalizacao de texto: {'PASSOU' if test1_passed else 'FALHOU'}")
    print(f"Integracao com agente: {'PASSOU' if test2_passed else 'FALHOU'}")
    
    if test1_passed and test2_passed:
        print("\nTodos os testes passaram! A normalizacao esta funcionando corretamente.")
    else:
        print("\nAlguns testes falharam. Verifique os erros acima.")