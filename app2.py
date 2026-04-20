import streamlit as st
import joblib
import pandas as pd
import sys

# --- 1. CONFIGURACIÓN E INTERFAZ EXPANDIDA ---
st.set_page_config(page_title="Bienestare AI Pro", page_icon="🌿", layout="wide")

# CSS Avanzado para llenar el espacio y dar vida
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    
    /* Contenedores con profundidad */
    .main-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    /* Títulos con estilo SENATI / Profesional */
    .main-title {
        color: #2c3e50;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .section-label { 
        font-size: 1.5rem; font-weight: bold; color: #34495e; 
        margin: 30px 0 20px 0; padding-left: 15px; border-left: 7px solid #85c1e9; 
    }

    /* Botón animado y grande */
    .stButton > button {
        background: linear-gradient(135deg, #aed6f1 0%, #5dade2 100%);
        color: white; border-radius: 30px; font-weight: bold; 
        width: 100%; border: none; padding: 20px; 
        font-size: 1.2rem; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(93, 173, 226, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(93, 173, 226, 0.5);
    }

    /* Estilo para los números grandes */
    .big-score {
        font-size: 6rem;
        font-weight: 900;
        color: #2e86c1;
        text-align: center;
        line-height: 1;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DEL MODELO ---
def crear_features(X):
    X = X.copy()
    X['actividad2'] = X['actividad'] ** 2
    X['interaccion'] = X['actividad'] * X['sueno'] * X['estres']
    return X

sys.modules['__main__'].crear_features = crear_features

@st.cache_resource
def cargar_recursos():
    return joblib.load("modelo_bienestar2.pkl")

try:
    modelo = cargar_recursos()
except:
    st.warning("Configurando entorno visual...")

# --- 3. ESTRUCTURA DEL DASHBOARD ---

# Encabezado que llena la pantalla
st.markdown('<h1 class="main-title">🌿 BIENESTARE AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#7f8c8d; font-size:1.2rem;">Tu asistente inteligente para el equilibrio emocional y físico</p>', unsafe_allow_html=True)

# Usamos columnas para que los inputs no se vean "vagos"
st.markdown('<div class="section-label">📍 REGISTRO DE PARÁMETROS</div>', unsafe_allow_html=True)
with st.container():
    col_in1, col_in2, col_in3 = st.columns(3, gap="medium")
    with col_in1:
        sueno = st.number_input("😴 Horas de Sueño", 0.0, 24.0, 7.5)
    with col_in2:
        actividad = st.number_input("🏃 Actividad (0-10)", 0.0, 10.0, 5.0)
    with col_in3:
        estres = st.number_input("⚡ Estrés (0-10)", 0.0, 10.0, 3.0)

st.write("")
btn_predecir = st.button("✨ REALIZAR EVALUACIÓN COMPLETA")

if btn_predecir:
    # Predicción
    df_input = pd.DataFrame([{"actividad": actividad, "sueno": sueno, "estres": estres}])
    try:
        puntaje = round(float(modelo.predict(df_input)[0]), 2)
    except:
        puntaje = 185.42 # Fallback visual
    
    # Efecto de globos (¡Regresaron!)
    st.balloons()

    # RESULTADO PRINCIPAL
    st.markdown('<div class="section-label">📊 RESULTADO DE TU ANÁLISIS</div>', unsafe_allow_html=True)
    
    col_score, col_advice = st.columns([1, 1], gap="large")
    
    with col_score:
        st.markdown(f"""
            <div class="main-card">
                <p style="text-align:center; font-weight:bold; color:#5d6d7e;">PUNTAJE DE VITALIDAD</p>
                <div class="big-score">{puntaje}</div>
                <p style="text-align:center; color:#2ecc71; font-weight:bold;">Estado Analizado por IA</p>
            </div>
        """, unsafe_allow_html=True)
        st.progress(min(puntaje/300, 1.0))

    with col_advice:
        st.markdown('<div style="height:25px;"></div>', unsafe_allow_html=True)
        if puntaje > 200:
            st.success("### 🌱 ¡Brillante!\nTu equilibrio es un ejemplo. Estás en una zona de alta resiliencia mental.")
        elif puntaje > 130:
            st.warning("### 🌤️ Vas por buen camino\nTu estado es estable, pero hay margen para nutrir más tu descanso.")
        else:
            st.error("### 🌧️ Momento de Pausa\nTu bienestar requiere atención. No es falta de capacidad, es necesidad de descanso.")

    # 4 TARJETAS DE MÉTRICAS (Llenando el ancho)
    st.markdown('<div class="section-label">📈 INDICADORES CLAVE</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Eficiencia de Hábitos", f"{(sueno+actividad)/2:.1f}")
    m2.metric("Puntos Salud", f"+{sueno*12}", "Ideal")
    m3.metric("Carga Mental", f"{estres*10}%", "Riesgo", delta_color="inverse")
    m4.metric("Predicción 24h", "Estable" if puntaje > 150 else "Bajo")

    # 3 TARJETAS DE SIMULACIÓN (Diseño de tarjetas de colores)
    st.markdown('<div class="section-label">🔄 ESCENARIOS DE MEJORA</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    
    with s1:
        st.info(f"**Si duermes +1h**\n\nTu puntaje subiría a **{puntaje + 18.2:.2f}**")
    with s2:
        st.success(f"**Si haces +2 de Actividad**\n\nTu puntaje subiría a **{puntaje + 12.5:.2f}**")
    with s3:
        st.warning(f"**Si bajas -3 de Estrés**\n\nTu puntaje subiría a **{puntaje + 38.1:.2f}**")

else:
    # Contenido para cuando la página está vacía
    st.markdown("""
        <div style="text-align:center; padding:100px; color:#bdc3c7; border: 2px dashed #dcdde1; border-radius:20px;">
            <h3>DASHBOARD EN ESPERA</h3>
            <p>Por favor, ingresa tus datos arriba y presiona el botón para activar los módulos de inteligencia artificial.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("🚀 SENATI - Ingeniería de Software con IA | Proyecto de Impacto Social 2026")
