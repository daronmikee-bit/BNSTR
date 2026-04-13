import streamlit as st
import joblib
import pandas as pd
import sys

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Bienestar AI Pro", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stNumberInput > div > div > input { background-color: #ffffff; border-radius: 10px; }
    .stButton > button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white; border-radius: 20px; font-weight: bold; width: 100%; border: none; padding: 10px;
    }
    .metric-container { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DEL MODELO (Antes en Flask) ---
def crear_features(X):
    X = X.copy()
    X['actividad2'] = X['actividad'] ** 2
    X['interaccion'] = X['actividad'] * X['sueno'] * X['estres']
    return X

# Necesario para que joblib encuentre la función al cargar el pkl
sys.modules['__main__'].crear_features = crear_features

@st.cache_resource
def cargar_recursos():
    modelo = joblib.load("modelo_bienestar2.pkl")
    return modelo

try:
    modelo = cargar_recursos()
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")

# --- 3. INTERFAZ DE USUARIO ---
st.title("🧠 Dashboard de Bienestar con IA")
st.write("Ingeniería de Software con IA - Análisis Predictivo")
st.markdown("---")

col_inputs, col_results = st.columns([1, 1.5], gap="large")

with col_inputs:
    st.subheader("📝 Registro de Datos")
    with st.container():
        actividad = st.number_input("🏃 Nivel de Actividad (0-10)", 0.0, 10.0, 5.0, step=0.1)
        sueno = st.number_input("😴 Horas de Sueño", 0.0, 24.0, 7.5, step=0.5)
        estres = st.number_input("⚡ Nivel de Estrés (0-10)", 0.0, 10.0, 3.0, step=0.1)
        
        btn_predecir = st.button("🚀 GENERAR DIAGNÓSTICO")

with col_results:
    if btn_predecir:
        # Preparar datos para el modelo
        df_input = pd.DataFrame([{
            "actividad": actividad,
            "sueno": sueno,
            "estres": estres
        }])
        
        # Predicción directa
        puntaje = round(float(modelo.predict(df_input)[0]), 2)
        
        # Mostrar resultados con estilo
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Puntaje de Bienestar Estimado", value=f"{puntaje} pts")
        
        # Barra de progreso dinámica (ajustada a escala ~250)
        progreso = min(puntaje / 300.0, 1.0)
        st.progress(progreso)
        
        # Consejos Inteligentes
        st.subheader("💡 Recomendaciones de la IA")
        if puntaje > 220:
            st.success("**Estado Óptimo:** Tu equilibrio actual es excelente. Mantén tus hábitos de descanso.")
        elif puntaje > 120:
            st.warning("**Estado Estable:** Estás bien, pero podrías mejorar optimizando tus horas de sueño.")
            if sueno < 7: st.write("- 🌙 Prioriza dormir al menos 7.5 horas hoy.")
        else:
            st.error("**Alerta de Desgaste:** El modelo detecta niveles de estrés/fatiga críticos.")
            st.write("- 🧘 Realiza una pausa activa y reduce estímulos visuales.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.balloons()
    else:
        st.info("Ingresa tus métricas diarias y presiona el botón para analizar.")

st.markdown("---")
st.caption("SENATI Ayacucho 2026 | Desarrollado por un futuro Ingeniero de Software")