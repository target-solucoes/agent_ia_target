"""
Script para validar se o setup do agente está funcionando corretamente
"""
import os
import sys
import pandas as pd
from pathlib import Path

def check_file_exists():
    """Verifica se o arquivo parquet existe"""
    data_path = "data/raw/DadosComercial_limpo.parquet"
    if os.path.exists(data_path):
        print(f"✓ Arquivo encontrado: {data_path}")
        return True
    else:
        print(f"✗ Arquivo não encontrado: {data_path}")
        return False

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = ['agno', 'pandas', 'pyarrow', 'duckdb', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} instalado")
        except ImportError:
            print(f"✗ {package} não encontrado")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def check_env_variables():
    """Verifica se as variáveis de ambiente estão configuradas"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("✓ OPENAI_API_KEY configurada")
        return True
    else:
        print("✗ OPENAI_API_KEY não encontrada")
        return False

def check_data_structure():
    """Verifica a estrutura dos dados"""
    data_path = "data/raw/DadosComercial_limpo.parquet"
    try:
        df = pd.read_parquet(data_path)
        print(f"✓ Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"  Colunas: {list(df.columns)}")
        print(f"  Tipos: {dict(df.dtypes)}")
        return True
    except Exception as e:
        print(f"✗ Erro ao carregar dados: {e}")
        return False

def check_agno_imports():
    """Verifica se as importações do Agno funcionam"""
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        from agno.tools.reasoning import ReasoningTools
        from agno.tools.duckdb import DuckDbTools
        from agno.knowledge.base import KnowledgeBase
        print("✓ Importações do Agno funcionando")
        return True
    except ImportError as e:
        print(f"✗ Erro nas importações do Agno: {e}")
        return False

def run_validation():
    """Executa todas as validações"""
    print("=== VALIDAÇÃO DO SETUP DO AGENTE ===\n")
    
    checks = [
        ("Arquivo de dados", check_file_exists),
        ("Dependências", lambda: check_dependencies()[0]),
        ("Variáveis de ambiente", check_env_variables),
        ("Estrutura dos dados", check_data_structure),
        ("Importações do Agno", check_agno_imports),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"Verificando {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Erro na verificação de {name}: {e}")
            results.append((name, False))
        print()
    
    # Resumo
    print("=== RESUMO DA VALIDAÇÃO ===")
    all_passed = True
    for name, passed in results:
        status = "✓ PASSOU" if passed else "✗ FALHOU"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print(f"\nStatus geral: {'✓ SETUP VÁLIDO' if all_passed else '✗ SETUP COM PROBLEMAS'}")
    return all_passed

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)