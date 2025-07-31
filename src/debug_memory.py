"""
Script de debug para testar a funcionalidade de memória contextual temporária do agente.
Este script simula as interações conforme especificado:
1. "meu nome é Pedro"
2. "qual é meu nome?"

O objetivo é verificar se o agente consegue lembrar informações da primeira interação
na segunda interação, demonstrando que a memória contextual está funcionando.
"""

import sys
import os
from datetime import datetime
import json

# Adicionar src ao path para importação
sys.path.append("src")
sys.path.append(".")

from duckdb_agent import create_agent
from dotenv import load_dotenv

load_dotenv()

def debug_memory_functionality():
    """
    Testa a funcionalidade de memória do agente com as frases especificadas
    """
    print("=" * 60)
    print("DEBUG: TESTE DE MEMORIA CONTEXTUAL TEMPORARIA")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Simular um ID de sessão único (como seria no Streamlit)
    session_id = f"debug_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"Session ID: {session_id}")
    print()

    # Criar agente com memoria
    print("Inicializando agente com memoria...")
    try:
        agent, df = create_agent(session_user_id=session_id)
        print("Agente inicializado com sucesso!")
        print(f"   - Dataset carregado: {len(df)} linhas")
        print(f"   - Agente configurado com memoria temporaria")
        print()
    except Exception as e:
        print(f"Erro ao inicializar agente: {e}")
        return False

    # Lista para armazenar o log da conversa
    conversation_log = []

    # TESTE 1: Primeira interacao - "meu nome eh Pedro"
    print("TESTE 1: Primeira interacao")
    print("-" * 40)
    
    first_query = "meu nome eh Pedro"
    print(f"Usuario: {first_query}")
    
    try:
        response1 = agent.run(first_query)
        print(f"Agente: {response1.content}")
        
        conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "query": first_query,
            "response": response1.content,
            "test": "Primeira interacao - estabelecer nome"
        })
        
        print("Primeira interacao processada com sucesso!")
        
    except Exception as e:
        print(f"Erro na primeira interacao: {e}")
        return False

    print()
    print("Aguardando antes da segunda interacao...")
    print()

    # TESTE 2: Segunda interacao - "qual eh meu nome?"
    print("TESTE 2: Segunda interacao")
    print("-" * 40)
    
    second_query = "qual eh meu nome?"
    print(f"Usuario: {second_query}")
    
    try:
        response2 = agent.run(second_query)
        print(f"Agente: {response2.content}")
        
        conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "query": second_query,
            "response": response2.content,
            "test": "Segunda interacao - recuperar nome da memoria"
        })
        
        print("Segunda interacao processada com sucesso!")
        
    except Exception as e:
        print(f"Erro na segunda interacao: {e}")
        return False

    print()
    
    # ANALISE DOS RESULTADOS
    print("ANALISE DOS RESULTADOS")
    print("-" * 40)
    
    # Verificar se o agente mencionou "Pedro" na segunda resposta
    second_response_lower = response2.content.lower()
    pedro_mentioned = "pedro" in second_response_lower
    
    if pedro_mentioned:
        print("SUCESSO: O agente lembrou do nome 'Pedro' na segunda interacao!")
        print("   A memoria contextual esta funcionando corretamente.")
        memory_test_passed = True
    else:
        print("FALHA: O agente NAO lembrou do nome 'Pedro' na segunda interacao.")
        print("   A memoria contextual pode nao estar funcionando.")
        memory_test_passed = False
    
    print()
    
    # TESTE ADICIONAL: Verificar se existe contexto de memoria
    print("TESTE ADICIONAL: Verificacao de contexto")
    print("-" * 40)
    
    context_query = "voce lembra de alguma informacao sobre mim?"
    print(f"Usuario: {context_query}")
    
    try:
        response3 = agent.run(context_query)
        print(f"Agente: {response3.content}")
        
        conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "query": context_query,
            "response": response3.content,
            "test": "Teste adicional - verificacao de contexto geral"
        })
        
    except Exception as e:
        print(f"Erro no teste adicional: {e}")

    print()
    
    # SALVAR LOG DA CONVERSA
    log_filename = f"sessions/{session_id}.json"
    os.makedirs("sessions", exist_ok=True)
    
    full_log = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "memory_test_passed": memory_test_passed,
        "conversation": conversation_log,
        "summary": {
            "first_query": first_query,
            "second_query": second_query,
            "pedro_mentioned_in_response": pedro_mentioned,
            "memory_functionality": "Working" if memory_test_passed else "Not Working"
        }
    }
    
    try:
        with open(log_filename, 'w', encoding='utf-8') as f:
            json.dump(full_log, f, ensure_ascii=False, indent=2)
        print(f"Log salvo em: {log_filename}")
    except Exception as e:
        print(f"Aviso: Nao foi possivel salvar o log: {e}")

    print()
    
    # RESUMO FINAL
    print("RESUMO FINAL")
    print("-" * 40)
    print(f"Session ID: {session_id}")
    print(f"Primeira pergunta: '{first_query}'")
    print(f"Segunda pergunta: '{second_query}'")
    print(f"Nome 'Pedro' lembrado: {'SIM' if pedro_mentioned else 'NAO'}")
    print(f"Teste de memoria: {'PASSOU' if memory_test_passed else 'FALHOU'}")
    
    if memory_test_passed:
        print("A implementacao de memoria contextual temporaria esta FUNCIONANDO!")
    else:
        print("A implementacao de memoria contextual precisa de AJUSTES.")
    
    print()
    print("=" * 60)
    
    return memory_test_passed


def test_memory_isolation():
    """
    Testa se a memoria eh isolada entre diferentes sessoes
    """
    print("TESTE DE ISOLAMENTO DE MEMORIA")
    print("-" * 40)
    
    # Criar duas sessoes diferentes
    session_1 = f"session_1_{datetime.now().strftime('%H%M%S')}"
    session_2 = f"session_2_{datetime.now().strftime('%H%M%S')}"
    
    print(f"Criando sessao 1: {session_1}")
    agent_1, _ = create_agent(session_user_id=session_1)
    
    print(f"Criando sessao 2: {session_2}")
    agent_2, _ = create_agent(session_user_id=session_2)
    
    # Estabelecer nome na sessao 1
    print(f"\n[Sessao 1]: meu nome eh Joao")
    response_1 = agent_1.run("meu nome eh Joao")
    print(f"[Sessao 1]: {response_1.content}")
    
    # Tentar recuperar nome na sessao 2 (deve falhar)
    print(f"\n[Sessao 2]: qual eh meu nome?")
    response_2 = agent_2.run("qual eh meu nome?")
    print(f"[Sessao 2]: {response_2.content}")
    
    # Verificar isolamento
    joao_mentioned = "joão" in response_2.content.lower() or "joao" in response_2.content.lower()
    
    if not joao_mentioned:
        print("SUCESSO: As sessoes estao isoladas corretamente!")
        print("   A sessao 2 nao tem acesso a memoria da sessao 1.")
    else:
        print("FALHA: As sessoes NAO estao isoladas!")
        print("   A sessao 2 conseguiu acessar a memoria da sessao 1.")
    
    return not joao_mentioned


if __name__ == "__main__":
    print("INICIANDO TESTES DE MEMORIA CONTEXTUAL...")
    print()
    
    # Teste principal
    memory_works = debug_memory_functionality()
    
    print()
    
    # Teste de isolamento
    isolation_works = test_memory_isolation()
    
    print()
    print("RESULTADO GERAL")
    print("-" * 40)
    print(f"Memoria contextual: {'OK' if memory_works else 'FALHOU'}")
    print(f"Isolamento de sessoes: {'OK' if isolation_works else 'FALHOU'}")
    
    if memory_works and isolation_works:
        print("\nTODOS OS TESTES PASSARAM!")
        print("A implementacao de memoria contextual temporaria esta funcionando perfeitamente.")
    else:
        print("\nALGUNS TESTES FALHARAM!")
        print("A implementacao precisa de ajustes.")
    
    print("\n" + "=" * 60)