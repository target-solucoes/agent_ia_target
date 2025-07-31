"""
Arquivo de debug para testar funcionalidades do agente com dados parquet
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.duckdb import DuckDbTools
from agno.knowledge.base import KnowledgeBase

import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def test_data_loading():
    """Testa o carregamento dos dados do parquet"""
    data_path = "data/raw/DadosComercial_limpo.parquet"
    try:
        df = pd.read_parquet(data_path)
        print(f"✓ Dados carregados com sucesso!")
        print(f"  - Linhas: {len(df)}")
        print(f"  - Colunas: {len(df.columns)}")
        print(f"  - Colunas: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"✗ Erro ao carregar dados: {e}")
        return None

def test_knowledge_base_creation(df):
    """Testa a criação da knowledge base"""
    try:
        knowledge_base = KnowledgeBase()
        dataset_info = f"""
        Dataset: DadosComercial_limpo.parquet
        Número de linhas: {len(df)}
        Número de colunas: {len(df.columns)}
        Colunas: {', '.join(df.columns.tolist())}
        """
        knowledge_base.add_text(dataset_info)
        print("✓ Knowledge base criada com sucesso!")
        return knowledge_base
    except Exception as e:
        print(f"✗ Erro ao criar knowledge base: {e}")
        return None

def test_agent_creation(knowledge_base, df):
    """Testa a criação do agente"""
    try:
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            description="Assistente de análise de dados comerciais",
            tools=[
                ReasoningTools(add_instructions=True),
                DuckDbTools(),
            ],
            knowledge_base=knowledge_base,
            instructions=f"Você tem acesso a dados comerciais com {len(df)} linhas.",
            show_tool_calls=True,
            markdown=True,
        )
        print("✓ Agente criado com sucesso!")
        return agent
    except Exception as e:
        print(f"✗ Erro ao criar agente: {e}")
        return None

def run_sample_queries(agent):
    """Executa queries de exemplo"""
    queries = [
        "Quantas linhas tem o dataset?",
        "Quais são as colunas disponíveis?",
        "Mostre as primeiras 3 linhas dos dados",
    ]
    
    for query in queries:
        print(f"\n🔍 Testando query: {query}")
        try:
            response = agent.run(query)
            print(f"✓ Query executada com sucesso!")
        except Exception as e:
            print(f"✗ Erro na query: {e}")

if __name__ == "__main__":
    print("=== DEBUG DO AGENTE COM DADOS PARQUET ===\n")
    
    # Teste 1: Carregamento dos dados
    print("1. Testando carregamento dos dados...")
    df = test_data_loading()
    if df is None:
        exit(1)
    
    # Teste 2: Criação da knowledge base
    print("\n2. Testando criação da knowledge base...")
    knowledge_base = test_knowledge_base_creation(df)
    if knowledge_base is None:
        exit(1)
    
    # Teste 3: Criação do agente
    print("\n3. Testando criação do agente...")
    agent = test_agent_creation(knowledge_base, df)
    if agent is None:
        exit(1)
    
    # Teste 4: Queries de exemplo
    print("\n4. Testando queries de exemplo...")
    run_sample_queries(agent)
    
    print("\n=== TESTES CONCLUÍDOS ===")