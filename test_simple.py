"""
Teste simples da normalizacao de texto
"""

import sys
import pandas as pd
sys.path.append("src")

from text_normalizer import TextNormalizer

def test_basic():
    print("Testando normalizacao basica...")
    
    normalizer = TextNormalizer()
    
    # Testes basicos
    tests = [
        ("MATRIZ SC", "matriz sc"),
        ("Sao Paulo", "sao paulo"), 
        ("  EMPRESA  ", "empresa"),
        ("", "")
    ]
    
    all_passed = True
    for original, expected in tests:
        result = normalizer.normalize_text(original)
        passed = result == expected
        print(f"'{original}' -> '{result}' {'OK' if passed else 'FAIL'}")
        if not passed:
            all_passed = False
    
    return all_passed

def test_dataframe():
    print("\nTestando DataFrame...")
    
    try:
        normalizer = TextNormalizer()
        df = pd.read_parquet('data/raw/DadosComercial_limpo.parquet')
        
        text_cols = normalizer.identify_text_columns(df)
        print(f"Colunas de texto: {text_cols}")
        
        df_norm = normalizer.normalize_dataframe(df, text_cols[:2])  # Apenas primeiras 2
        
        print("DataFrame normalizado com sucesso")
        return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste de Normalizacao ===")
    
    test1 = test_basic()
    test2 = test_dataframe()
    
    print(f"\nResultados:")
    print(f"Normalizacao basica: {'PASSOU' if test1 else 'FALHOU'}")
    print(f"DataFrame: {'PASSOU' if test2 else 'FALHOU'}")
    
    if test1 and test2:
        print("\nSUCESSO: Normalizacao funcionando!")
    else:
        print("\nFALHA: Verificar implementacao")