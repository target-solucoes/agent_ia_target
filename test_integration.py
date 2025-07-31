#!/usr/bin/env python3
"""
Script de teste para verificar a integração entre o agente e os dados
"""

import pandas as pd
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.duckdb import DuckDbTools

def test_data_loading():
    """Test data loading functionality"""
    print("* Testando carregamento dos dados...")
    try:
        df = pd.read_parquet("data/raw/DadosComercial_limpo.parquet")
        print(f"[OK] Dados carregados com sucesso: {df.shape}")
        print(f"* Colunas: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"[ERRO] Erro ao carregar dados: {e}")
        return None

def test_agent_initialization():
    """Test agent initialization"""
    print("\n* Testando inicializacao do agente...")
    try:
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            description="You are an assistant please reply based on the question",
            tools=[
                ReasoningTools(add_instructions=True),
                DuckDbTools(),
            ],
            instructions="Use tables to display data",
            show_tool_calls=True,
            markdown=True,
        )
        print("[OK] Agente inicializado com sucesso")
        return agent
    except Exception as e:
        print(f"[ERRO] Erro ao inicializar agente: {e}")
        return None

def test_integration(df, agent):
    """Test integration between agent and data"""
    print("\n* Testando integracao agente + dados...")
    try:
        import duckdb
        conn = duckdb.connect(':memory:')
        conn.register('DadosComercial_limpo', df)
        print("[OK] Dados registrados no DuckDB")
        
        # Test simple query
        result = conn.execute("SELECT COUNT(*) as total FROM DadosComercial_limpo").fetchone()
        print(f"* Total de registros no DuckDB: {result[0]}")
        
        return True
    except Exception as e:
        print(f"[ERRO] Erro na integracao: {e}")
        return False

if __name__ == "__main__":
    print("* Iniciando testes de integracao...")
    
    # Test data loading
    df = test_data_loading()
    if df is None:
        exit(1)
    
    # Test agent initialization
    agent = test_agent_initialization()
    if agent is None:
        exit(1)
    
    # Test integration
    integration_ok = test_integration(df, agent)
    if not integration_ok:
        exit(1)
    
    print("\n[SUCESSO] Todos os testes passaram! A integracao esta funcionando.")
    print("\n* Para executar o app Streamlit:")
    print("   streamlit run app.py")