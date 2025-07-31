# 🤖 Target AI Agent - Interface Streamlit

## 📋 Descrição

Interface web desenvolvida em Streamlit que integra o agente Agno com os dados comerciais em formato Parquet. A aplicação oferece uma interface de chat interativa onde o agente pode analisar e responder perguntas sobre os dados.

## ✅ Problema Resolvido

- ✅ **Carregamento automático** do arquivo `data/raw/DadosComercial_limpo.parquet`
- ✅ **Integração completa** com o agente definido em `src/simple_agent.py`
- ✅ **Tratamento robusto de encoding** para evitar erros de codificação
- ✅ **Interface web intuitiva** com Streamlit
- ✅ **Disponibilização dos dados** via DuckDB para o agente

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install pyarrow fastparquet chardet
```

### 2. Configurar Variáveis de Ambiente

Certifique-se de que o arquivo `.env` contém:
```
OPENAI_API_KEY=sua_chave_aqui
```

### 3. Executar Testes de Integração

```bash
python test_integration.py
```

### 4. Executar a Aplicação Streamlit

```bash
streamlit run app.py
```

A aplicação estará disponível em: `http://localhost:8501`

## 📊 Dados

- **Arquivo**: `data/raw/DadosComercial_limpo.parquet`
- **Tamanho**: 5.542.646 linhas × 17 colunas
- **Colunas disponíveis**:
  - Empresa
  - Data_Emissao
  - Data_Entrega
  - Cod_Produto
  - Cod_Familia_Produto
  - Cod_Grupo_Produto
  - Cod_Linha_Produto
  - Peso_Unitario
  - Cod_Vendedor
  - Cod_Regiao_Vendedor
  - Cod_Cliente
  - UF_Cliente
  - Municipio_Cliente
  - Cod_Segmento_Cliente
  - Valor_Vendido
  - Peso_Vendido
  - Qtd_Vendida

## 🔧 Funcionalidades

### Interface Principal
- **Status em tempo real** do carregamento dos dados e agente
- **Preview dos dados** com informações detalhadas das colunas
- **Estatísticas do dataset** (linhas, colunas, uso de memória)

### Chat Interativo
- **Interface de chat** para interagir com o agente
- **Acesso completo aos dados** via DuckDB
- **Histórico de conversas** mantido durante a sessão
- **Processamento com feedback visual** (spinner de loading)

### Tratamento de Erros
- **Carregamento robusto** com tratamento de encoding
- **Mensagens de erro informativas**
- **Fallbacks automáticos** para diferentes engines de leitura

## 🛠️ Arquitetura

```
app.py
├── load_parquet_data()     # Carrega dados com tratamento de encoding
├── initialize_agent()      # Inicializa agente Agno
├── main()                  # Interface principal Streamlit
└── Chat Interface          # Sistema de chat interativo
```

## ⚡ Performance

- **Cache de dados**: `@st.cache_data` para carregamento único
- **Cache de agente**: `@st.cache_resource` para reutilização
- **Processamento em memória**: DuckDB para queries rápidas
- **Interface responsiva**: Colunas adaptáveis e componentes otimizados

## 🔍 Exemplos de Uso

Você pode fazer perguntas como:

- "Quantos registros temos no dataset?"
- "Quais são as principais empresas por volume de vendas?"
- "Mostre um resumo dos dados por região"
- "Qual o produto mais vendido?"
- "Analise as vendas por mês"

## 🐛 Solução de Problemas

### Erro de Encoding
Se encontrar erros de encoding, o sistema automaticamente:
1. Tenta diferentes engines (PyArrow, FastParquet)
2. Aplica limpeza de caracteres problemáticos
3. Usa tratamento `errors='ignore'` para caracteres inválidos

### Agente não Inicializa
- Verifique se `OPENAI_API_KEY` está configurado no `.env`
- Confirme se todas as dependências estão instaladas
- Execute `python test_integration.py` para diagnóstico

### Porta em Uso
Se a porta 8501 estiver ocupada:
```bash
streamlit run app.py --server.port 8502
```

## 📁 Estrutura de Arquivos

```
├── app.py                          # Aplicação Streamlit principal
├── src/simple_agent.py             # Agente original (não modificado)
├── data/raw/DadosComercial_limpo.parquet  # Dados comerciais
├── test_integration.py             # Script de testes
├── pyproject.toml                  # Dependências do projeto
└── README_STREAMLIT.md             # Esta documentação
```

## ✨ Recursos Técnicos

- **Framework**: Streamlit + Agno
- **Processamento de dados**: Pandas + DuckDB
- **LLM**: OpenAI GPT-4o-mini
- **Leitura de arquivos**: PyArrow/FastParquet
- **Interface**: Chat interativo com histórico
- **Deployment**: Local via Streamlit server