import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

# --- Menú lateral ---
st.sidebar.header("Configuración del modelo")

# Slider para temperatura
temperatura = st.sidebar.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Select para modelo
modelo_seleccionado = st.sidebar.selectbox(
    "Selecciona el modelo",
    ["gemini-2.5-flash", "gemini-1.0", "otro-modelo"]  # Ajusta según los modelos disponibles
)

# Botón para limpiar conversación
if st.sidebar.button("Limpiar conversación"):
    st.session_state.mensajes = []

# Crear el modelo con la configuración seleccionada
chat_model = ChatGoogleGenerativeAI(model=modelo_seleccionado, temperature=temperatura)

# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Renderizar historial existente
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)
