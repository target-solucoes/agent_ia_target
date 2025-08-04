import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import warnings
import sys
import uuid

sys.path.append("src")
from duckdb_agent import create_agent
from text_normalizer import TextNormalizer

warnings.filterwarnings("ignore")

load_dotenv()

# Page configuration
st.set_page_config(page_title="Agente IA Target", page_icon="🤖", layout="wide")


@st.cache_data
def load_parquet_data():
    """Carrega arquivo Parquet com tratamento robusto de codificação"""
    data_path = "data/raw/DadosComercial_resumido.parquet"

    # Method 1: Try direct pandas loading
    try:
        with st.spinner("🔄 Carregando dados..."):
            df = pd.read_parquet(data_path)

            # Process string columns for encoding issues
            string_cols = df.select_dtypes(include=["object"]).columns
            for col in string_cols:
                try:
                    # Convert to string and clean encoding
                    original_values = df[col].fillna("")
                    cleaned_values = []

                    for val in original_values:
                        if isinstance(val, bytes):
                            # Handle bytes
                            try:
                                cleaned_val = val.decode("utf-8", errors="replace")
                            except:
                                cleaned_val = str(val)
                        else:
                            # Handle strings with potential encoding issues
                            cleaned_val = (
                                str(val)
                                .encode("utf-8", errors="ignore")
                                .decode("utf-8")
                            )
                        cleaned_values.append(cleaned_val)

                    df[col] = cleaned_values

                except Exception as col_error:
                    # If column processing fails, keep original
                    st.warning(
                        f"⚠️ Mantendo coluna {col} original devido a: {col_error}"
                    )
                    continue

            return df, None

    except Exception as e:
        return None, f"Erro ao carregar dados: {str(e)}"


@st.cache_resource
def initialize_agent():
    """Inicializa o agente DuckDB configurado com memória temporária baseada em sessão"""
    try:
        # Gerar um ID único para a sessão do Streamlit se não existir
        if "session_user_id" not in st.session_state:
            st.session_state.session_user_id = str(uuid.uuid4())

        agent, df_agent = create_agent(session_user_id=st.session_state.session_user_id)
        return agent, df_agent, None
    except Exception as e:
        return None, None, str(e)


def main():
    # Enhanced CSS for professional styling
    st.markdown(
        """
    <style>
    .main > div {
        padding-top: 1rem;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .app-title {
        color: white !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 2.5rem;
        font-weight: 300;
        margin: 0;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .app-subtitle {
        color: white !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1rem;
        font-weight: 300;
        margin: 0.5rem 0 0 0;
        letter-spacing: 1px;
        opacity: 0.95;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .app-description {
        color: rgba(255,255,255,0.8);
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.9rem;
        font-weight: 300;
        margin: 1rem 0 0 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }
    
    .feature-icons {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .feature-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: rgba(255,255,255,0.7);
        font-size: 0.8rem;
        font-weight: 300;
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    /* Chat Container Styling */
    .chat-main-container {
        display: flex;
        flex-direction: column;
        margin: 2rem 0;
    }
    
    .chat-messages-container {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 15px;
        border: 1px solid var(--secondary-background-color);
    }
    
    .chat-input-container {
        padding: 1.5rem 0;
        margin-top: 1rem;
        border-top: 1px solid var(--secondary-background-color);
    }
    
    /* Chat Message Styling - Dark mode friendly */
    .stChatMessage {
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid var(--secondary-background-color);
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        color: white !important;
        margin-left: 2rem;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        border-left: 4px solid #e74c3c;
        margin-right: 2rem;
    }
    
    /* Chat Input Styling - Dark mode friendly */
    .stChatInputContainer {
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        background: transparent;
    }
    
    .stChatInput > div {
        border-radius: 25px !important;
        border: 2px solid #e74c3c !important;
    }
    
    .stChatInput input {
        border: none !important;
        font-size: 1rem !important;
        padding: 1rem 1.5rem !important;
    }
    
    /* Welcome message styling - Dark mode friendly */
    .welcome-message {
        text-align: center;
        padding: 3rem 2rem;
        font-style: italic;
        border-radius: 15px;
        margin: 2rem 0;
        border: 2px dashed var(--secondary-background-color);
    }
    
    .welcome-message h3 {
        color: #e74c3c;
        margin-bottom: 1rem;
    }
    
    
    /* Delete Chat Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.4rem 0.8rem;
        font-weight: 400;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(108, 117, 125, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6268 0%, #495057 100%);
        transform: translateY(-1px);
        box-shadow: 0 3px 12px rgba(108, 117, 125, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        .feature-icons {
            gap: 1rem;
        }
        .header-container {
            padding: 1.5rem 1rem;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Import selected_model from duckdb_agent
    from duckdb_agent import selected_model

    # Enhanced Professional Header
    st.markdown(
        f"""
        <div class="header-container">
            <h1 class="app-title">🤖 AGENTE IA TARGET</h1>
            <p class="app-subtitle">INTELIGÊNCIA ARTIFICIAL PARA ANÁLISE DE DADOS</p>
            <p class="app-description">
                Converse naturalmente com seus dados comerciais. Faça perguntas em linguagem natural 
                e obtenha insights precisos através de análise inteligente.<br>
                <small style="opacity: 0.7;">Modelo: {selected_model}</small>
            </p>
            <div class="feature-icons">
                <div class="feature-item">
                    <div class="feature-icon">💬</div>
                    <span>Chat Natural</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">📊</div>
                    <span>Análise Rápida</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🎯</div>
                    <span>Insights Precisos</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🚀</div>
                    <span>Resultados Instantâneos</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load data and agent silently
    df, data_error = load_parquet_data()
    agent, df_agent, agent_error = initialize_agent()

    # Enhanced Chat interface
    if agent is not None and df is not None:
        # Center the chat interface
        chat_col1, chat_col2, chat_col3 = st.columns([1, 3, 1])

        with chat_col2:
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
                # Add welcome message as first assistant message
                welcome_msg = """👋 Olá! Sou o **Agente IA Target**, seu assistente para análise de dados comerciais.

Estou aqui para ajudá-lo a explorar e entender seus dados através de conversas naturais. Você pode me fazer perguntas como:
- "Quais são os produtos mais vendidos?"
- "Mostre o faturamento por região"
- "Analise as tendências de vendas"

Como posso ajudá-lo hoje?"""
                st.session_state.messages.append(
                    {"role": "assistant", "content": welcome_msg}
                )

            # Initialize session user ID for memory if not exists
            if "session_user_id" not in st.session_state:
                st.session_state.session_user_id = str(uuid.uuid4())

            # Delete Chat button
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🗑️ Limpar", type="secondary"):
                    # Clear all session state related to chat
                    st.session_state.messages = []
                    if "session_user_id" in st.session_state:
                        del st.session_state.session_user_id
                    # Force app rerun to refresh everything
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Display chat messages with improved styling
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # Process user input first
            if prompt := st.chat_input(
                "💬 Faça sua pergunta sobre os dados comerciais..."
            ):
                # Add user message to chat history and display
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Get agent response
                with st.spinner("🤔 Analisando..."):
                    try:
                        response = agent.run(prompt)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response.content}
                        )
                    except Exception as e:
                        error_msg = f"❌ Erro ao processar: {str(e)}"
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_msg}
                        )
                
                # Rerun to display new messages
                st.rerun()
    else:
        st.error("⚠️ Erro ao inicializar o sistema. Recarregue a página.")
        if data_error:
            st.error(f"Dados: {data_error}")
        if agent_error:
            st.error(f"Agente: {agent_error}")

    # --- Footer Target Data Experience ---
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    # Criação do footer com logotipo
    footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

    with footer_col2:
        from PIL import Image
        import base64
        import io

        # Texto do footer
        # Fallback caso a imagem não seja encontrada
        st.markdown(
            """
            <div style="text-align: center; background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%); 
                        padding: 30px; border-radius: 15px; margin: 20px 0; display: flex; 
                        flex-direction: column; align-items: center; justify-content: center;">
                <div style="color: white; font-family: 'Arial', sans-serif; font-weight: 300; 
                           letter-spacing: 6px; margin: 0; font-size: 24px;">T A R G E T</div>
                <div style="color: #e74c3c; font-family: 'Arial', sans-serif; font-weight: 300; 
                          letter-spacing: 3px; margin: 8px 0 0 0; font-size: 12px;">D A T A &nbsp; E X P E R I E N C E</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
