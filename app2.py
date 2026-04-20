import streamlit as st
import joblib
import pandas as pd
import sys

# --- 1. CONFIGURACIÓN Y ESTILO PASTEL (PSICOLOGÍA DEL COLOR) ---
st.set_page_config(page_title="Bienestare AI - Dashboard Calma", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    /* Fondo general en tono hueso/crema muy suave */
    .stApp { background-color: #fdfbf7; }
    
    /* Títulos con bordes suaves y colores pastel */
    .section-label { 
        font-size: 1.3rem; font-weight: bold; color: #5d6d7e; 
        margin: 25px 0 15px 0; padding-left: 10px; border-left: 5px solid #aed6f1; 
    }
    
    /* Botón con degradado suave (Azul pastel) */
    .stButton > button {
        background: linear-gradient(90deg, #aed6f1 0%, #85c1e9 100%);
        color: #1b4f72; border-radius: 25px; font-weight: bold; 
        width: 100%; border: none; padding: 12px; transition: 0.3s;
    }
    .stButton > button:hover { transform: scale(1.02); opacity: 0.9; }

    /* Tarjetas de resultados (Blanco puro con sombra sutil) */
    .metric-card { 
        background-color: white; padding: 20px; border-radius: 20px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #eaf2f8;
        text-align: center;
    }
    
    /* Caja de alertas con colores no agresivos */
    .stAlert { border-radius: 15px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DEL MODELO (INTACTA) ---
def crear_features(X):
    X = X.copy()
    X['actividad2'] = X['actividad'] ** 2
    X['interaccion'] = X['actividad'] * X['sueno'] * X['estres']
    return X

sys.modules['__main__'].crear_features = crear_features

@st.cache_resource
def cargar_recursos():
    # Asegúrate de que el nombre del archivo en GitHub sea exactamente este
    modelo = joblib.load("modelo_bienestar2.pkl")
    return modelo

try:
    modelo = cargar_recursos()
except Exception as e:
    st.error(f"Esperando conexión con el modelo... {e}")

# --- 3. INTERFAZ DE USUARIO (DASHBOARD COMPLETO) ---
st.title("🌿 Bienestare AI: Tu Espacio de Equilibrio")
st.write("Análisis predictivo diseñado para tu tranquilidad y bienestar emocional.")

# Fila superior: Inputs
st.markdown('<div class="section-label">📋 TUS MÉTRICAS DE HOY</div>', unsafe_allow_html=True)
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    sueno = st.number_input("😴 Horas de Sueño", 0.0, 24.0, 7.5, step=0.5)
with col_in2:
    actividad = st.number_input("🏃 Nivel de Actividad (0-10)", 0.0, 10.0, 5.0, step=0.1)
with col_in3:
    estres = st.number_input("⚡ Nivel de Estrés (0-10)", 0.0, 10.0, 3.0, step=0.1)

st.write("")
btn_predecir = st.button("🚀 GENERAR ANÁLISIS")

if btn_predecir:
    # Preparar datos
    df_input = pd.DataFrame([{"actividad": actividad, "sueno": sueno, "estres": estres}])
    puntaje = round(float(modelo.predict(df_input)[0]), 2)
    
    # --- RESULTADO PRINCIPAL ---
    st.markdown('<div class="section-label">📊 DIAGNÓSTICO INTEGRAL</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card">
            <p style="color: #7f8c8d; margin-bottom: 0;">PUNTAJE DE VITALIDAD</p>
            <h1 style="font-size: 4.5rem; color: #5499c7; margin: 0;">{puntaje}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(min(puntaje / 300.0, 1.0))

    # --- 4 TARJETAS DE ESTADÍSTICAS (COMO TU DISEÑO) ---
    st.markdown('<div class="section-label">📈 ESTADÍSTICAS RELACIONADAS</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Media Hábitos", f"{(sueno+actividad+(10-estres))/3:.1f}")
    with c2:
        st.metric("Factor Positivo", f"+{sueno*10}", delta="Saludable")
    with c3:
        # Usamos delta_color="inverse" para que el estrés se vea en rojo suave si sube
        st.metric("Carga Estrés", f"-{estres*12}", delta="Penalización", delta_color="inverse")
    with c4:
        st.metric("Balance IA", "Estable" if puntaje > 140 else "Revisar")

    # --- 3 TARJETAS DE SIMULACIÓN (ESCENARIOS MEJORADOS) ---
    st.markdown('<div class="section-label">🔄 ¿QUÉ PASARÍA SI MEJORAS UN POCO?</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    
    with s1:
        st.markdown(f"""<div style="background:#e8f8f5; padding:15px; border-radius:15px; text-align:center;">
            <p style="font-size:0.8rem; color:#16a085;">Si duermes +1h</p>
            <h3 style="margin:0; color:#16a085;">{puntaje + 18.4:.2f}</h3>
            <span style="font-size:0.8rem; font-weight:bold;">+18.4 Puntos</span>
        </div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""<div style="background:#fef9e7; padding:15px; border-radius:15px; text-align:center;">
            <p style="font-size:0.8rem; color:#f1c40f;">Actividad Física +2</p>
            <h3 style="margin:0; color:#b7950b;">{puntaje + 12.0:.2f}</h3>
            <span style="font-size:0.8rem; font-weight:bold;">+12.0 Puntos</span>
        </div>""", unsafe_allow_html=True)
    with s3:
        st.markdown(f"""<div style="background:#f4ecf7; padding:15px; border-radius:15px; text-align:center;">
            <p style="font-size:0.8rem; color:#8e44ad;">Estrés -3</p>
            <h3 style="margin:0; color:#8e44ad;">{puntaje + 35.8:.2f}</h3>
            <span style="font-size:0.8rem; font-weight:bold;">+35.8 Puntos</span>
        </div>""", unsafe_allow_html=True)

    # --- RECOMENDACIONES Y ALERTAS ---
    st.markdown('<div class="section-label">🚨 CENTRO DE ORIENTACIÓN</div>', unsafe_allow_html=True)
    if puntaje > 220:
        st.success("**¡Excelente equilibrio!** Tu mente y cuerpo están en sintonía. Sigue así.")
    elif puntaje > 120:
        st.warning("**Buen progreso.** Considera descansar un poco más para elevar tu energía.")
    else:
        st.error("**Momento de cuidar de ti.** Tus niveles indican que necesitas un descanso urgente. No te exijas de más hoy.")

else:
    st.info("Ingresa tus datos y presiona el botón para que la IA genere tu reporte de bienestar.")

st.markdown("---")
st.caption("SENATI Ayacucho 2026 | Tecnología con Propósito Humano")
