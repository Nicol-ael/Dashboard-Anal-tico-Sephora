import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# ======================================================
# CONFIGURACIÓN DE LA PÁGINA (LOOK EDITORIAL CLARO)
# ======================================================
st.set_page_config(
    page_title="Sephora Business Intelligence",
    page_icon="💄",
    layout="wide"
)

# ======================================================
# CARGA Y PREPROCESAMIENTO DE DATOS
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_csv("sephora_dashboard_data.csv")
    df["submission_time"] = pd.to_datetime(df["submission_time"], errors="coerce")
    df["year"] = df["submission_time"].dt.year
    df["loves_count"] = pd.to_numeric(df["loves_count"], errors="coerce").fillna(0)
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce").fillna(0)
    df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce").fillna(0)
    df["helpfulness"] = pd.to_numeric(df["helpfulness"], errors="coerce").fillna(0)
    
    # Estandarizar la columna de recommendations
    df["is_recommended"] = df["is_recommended"].astype(str).str.strip().str.lower()
    return df

df = load_data()

# Mapeo flexible para identificar los formatos de recomendación
mapeo_rec = {
    'true': 'Recomendado', '1': 'Recomendado', '1.0': 'Recomendado', 'recomendado': 'Recomendado', 'yes': 'Recomendado',
    'false': 'No Recomendado', '0': 'No Recomendado', '0.0': 'No Recomendado', 'no recomendado': 'No Recomendado', 'no': 'No Recomendado'
}
df["estado_recomendacion"] = df["is_recommended"].map(mapeo_rec).fillna("No Especificado")

# CÁLCULOS MATEMÁTICOS GLOBALES
productos_stats = df.groupby("product_name").agg(
    rating_promedio=("review_rating", "mean"),
    total_reviews=("review_rating", "count")
).reset_index()
productos_criticos = productos_stats[productos_stats["total_reviews"] >= 10]

# ======================================================
# DISEÑO CSS - CARGA DE ESTILOS GLOBALES
# ======================================================
st.markdown("""
<style>
            
            
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;500;600;700;800&display=swap');

/* Reset global - Tipografía limpia */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Montserrat', sans-serif !important;
}

/* Fondo Blanco de Boutique para la aplicación */
.stApp {
    background-color: #FFFFFF; 
    color: #121212;
}

/* Títulos principales y Subheaders con negrilla pura y limpia */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    color: #000000 !important;
    letter-spacing: -0.5px;
    background: transparent !important;
}

h4, strong {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;
    color: #000000 !important;
}

/* Texto normal */
/* TEXTO NORMAL SOLAMENTE */

p {
    color: #121212;
}

span {
    color: inherit !important;
}

label {
    color: inherit !important;
}
}

/* BARRA LATERAL (SIDEBAR) - Minimalista Black & White de Sephora */
section[data-testid="stSidebar"] {
    background-color: #000000 !important; 
    border-right: 1px solid #e0e0e0 !important;
}

section[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
    text-transform: uppercase;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    border-bottom: 1px solid #222;
    padding-bottom: 10px;
}

.sidebar-section-title {
    color: #ff4b91 !important;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #222;
    padding-bottom: 3px;
}

section[data-testid="stSidebar"] label p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    font-size: 0.75rem !important;
    letter-spacing: 1px;
}

/* TARJETAS KPI FIJAS (FILA INFERIOR) */
.kpi-card {
    background-color: #121214 !important;
    border: 1px solid #1c1c1f !important;
    border-top: 4px solid #000000 !important; 
    border-radius: 4px !important; 
    padding: 1.4rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.15) !important;
}

.kpi-card .kpi-title {
    color: #a1a1aa !important; 
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.kpi-card .kpi-value, .kpi-card div, .kpi-card span {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

.kpi-card .kpi-value {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.2rem;
    margin-top: 0.4rem;
}

/* CONTENEDOR DEL SIMULADOR DE PRICING */
.simulation-box {
    background-color: #000000 !important; 
    border: 1px solid #1c1c1f !important;
    padding: 1.8rem;
    margin-bottom: 0px !important;
    border-radius: 4px 4px 0px 0px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
}

.simulation-box h3, .simulation-box h3 span {
    color: #FFFFFF !important; 
}

.simulation-box p {
    color: #E4E4E7 !important; 
}

/* 🎯 NUEVAS TARJETAS CUSTOM POR INFRAESTRUCTURA HTML DIRECTA (BLANCO TOTAL INMUNE) 🎯 */
.custom-metric-card {
    background-color: #000000 !important;
    border: 1px solid #1c1c1f !important;
    padding: 20px !important;
    border-radius: 0px 0px 4px 4px;
    text-align: left;
}

.custom-metric-label {
    color: #A1A1AA !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 8px !important;
    display: block;
}

.custom-metric-value {
    color: #FFFFFF !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    margin-bottom: 6px !important;
    display: block;
}

.custom-metric-delta {
    color: #E4E4E7 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    display: block;
}

/* RECUADROS DE TEXTO INFORMATIVOS */
.insight {
    background-color: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-left: 4px solid #000000 !important;
    border-radius: 4px;
    padding: 1.2rem;
    margin-top: 1rem;
    box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.05) !important;
}

/* CUADROS PREMIUM DE CONCLUSIONES FINALES */
.premium-conclusion-box {
    background-color: #121214 !important;
    border: 1px solid #1c1c1f !important;
    padding: 1.5rem;
    border-radius: 4px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2) !important;
}
.premium-conclusion-box h4 {
    color: #FFFFFF !important;
    margin-top: 0px;
}
.premium-conclusion-box p, .premium-conclusion-box div {
    color: #e4e4e7 !important; 
}

/* AVATARES PERFILES DE PIEL CIRCULARES */
.avatar-box {
    background-color: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 50%; 
    width: 140px;
    height: 140px;
    margin: 0 auto 15px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4.5rem;
    box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1) !important;
}

/* BOTONES EDITORIALES SEPHORA */
/* BOTONES PREMIUM */

.stButton > button {
    background: #000000 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #2a2a2a !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    padding: 14px 18px !important;
    width: 100% !important;

    opacity: 1 !important;
    filter: none !important;

    -webkit-text-fill-color: #FFFFFF !important;

    box-shadow: 0 4px 15px rgba(0,0,0,0.18) !important;
}

.stButton > button:hover {
    background: #1a1a1a !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* SLIDERS STREAMLIT */
div[data-testid="stSlider"] div[role="slider"] { background-color: #000000 !important; border: 2px solid #ffffff !important; }
div[data-testid="stSlider"] .st-eb { background-color: #000000 !important; }
div[data-testid="stSlider"] label p { color: #000000 !important; font-weight: 700 !important; }

.footer { text-align: center; color: #000000 !important; font-weight: 700; margin-top: 5rem; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; border-top: 2px solid #000000; padding-top: 20px; }
[data-testid="stMarkdownContainer"] h1
            </style>
""", unsafe_allow_html=True)

# CONFIGURACIÓN GENERAL GRÁFICAS PLOTLY
layout_charts_editorial = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#000000", family="Montserrat", size=11),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#000000", weight="bold"), title_font=dict(size=11, color="#000000", weight="bold")),
    yaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#000000", weight="bold"), title_font=dict(size=11, color="#000000", weight="bold"))
)

# ======================================================
# SIDEBAR - CONFIGURACIÓN DEL MENÚ Y FILTROS
# ======================================================
with st.sidebar:
    # --- INYECCIÓN DE CSS PARA LOGRAR EL SIDEBAR NEGRO Y LETRAS BLANCAS ---
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #000000 !important;
            }
            [data-testid="stSidebar"] .stText, 
            [data-testid="stSidebar"] label, 
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] h2 {
                color: #ffffff !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: #27272a !important;
            }
            .sidebar-section-title {
                color: #ffffff !important;
                font-weight: 700;
                margin-top: 15px;
                margin-bottom: 5px;
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 1px;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] label p {
                color: #ffffff !important;
            }
            [data-testid="stSidebar"] div[data-testid="stThumbValue"],
            [data-testid="stSidebar"] div[data-testid="stTickBarMinMax"] {
                color: #a1a1aa !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- TITULO DE LA MARCA ---
    st.markdown(
        """
        <h2 style="
        text-align:center;
        margin-top:20px;
        margin-bottom:30px;
        font-size:4rem;
        letter-spacing:8px;
        font-family:'Playfair Display', serif;
        color: #ffffff;
        ">
        SEPHORA
        </h2>
        """,
        unsafe_allow_html=True
    )
    
    # --- MENÚ DE NAVEGACIÓN (SIEMPRE VISIBLE) ---
    menu = st.radio("Navegación del Sistema", ["Análisis del Catálogo", "Perfil de la Clienta", "Salud de Marca"])
    st.markdown("---")

    # --- FILTROS GLOBALES (AHORA SIEMPRE VISIBLES EN CUALQUIER PÁGINA) ---
    st.markdown("<div class='sidebar-section-title'>Métricas Comerciales</div>", unsafe_allow_html=True)
    rating_filter = st.slider("Calificación mínima (Rating)", float(df["review_rating"].min()), float(df["review_rating"].max()), 1.0)
    price_filter = st.slider("Precio máximo (USD)", 0, int(df["price_usd"].max()), int(df["price_usd"].max()) + 100)
    loves_filter = st.slider("Volumen mínimo de 'Loves'", 0, int(df["loves_count"].max()), 0, step=1000)

    st.markdown("<div class='sidebar-section-title'>Atributos de Catálogo</div>", unsafe_allow_html=True)
    category_filter = st.selectbox("Categoría de producto", ["Todas"] + sorted(df["primary_category"].dropna().unique().tolist()))
    brand_filter = st.selectbox("Marca / Fabricante", ["Todas"] + sorted(df["brand_name"].dropna().unique().tolist()))
    year_filter = st.selectbox("Año de registro", ["Todos"] + sorted(df["year"].dropna().astype(str).unique().tolist()))
    
    st.markdown("<br>", unsafe_allow_html=True)
    rec_filter = st.radio("Filtrar por Recommendation", ["Todos", "Recomendados", "No Recomendados"])
# ======================================================
# PÁGINA 1: TABLERO GENERAL + SIMULADOR PREDICTIVO
# ======================================================
if menu == "Análisis del Catálogo":
    
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df["review_rating"] >= rating_filter]
    filtered_df = filtered_df[filtered_df["price_usd"] <= price_filter]
    filtered_df = filtered_df[filtered_df["loves_count"] >= loves_filter]

    if category_filter != "Todas": filtered_df = filtered_df[filtered_df["primary_category"] == category_filter]
    if brand_filter != "Todas": filtered_df = filtered_df[filtered_df["brand_name"] == brand_filter]
    if year_filter != "Todos": filtered_df = filtered_df[filtered_df["year"] == int(year_filter)]

    if rec_filter == "Recomendados": filtered_df = filtered_df[filtered_df["estado_recomendacion"] == "Recomendado"]
    elif rec_filter == "No Recomendados": filtered_df = filtered_df[filtered_df["estado_recomendacion"] == "No Recomendado"]

    try:
        image = Image.open("image.jpg")
        st.image(image, use_container_width=True)
    except:
        st.markdown("<div style='background-color:#000000; height: 5px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    st.title("Dashboard de Análisis de Datos: Catálogo Sephora")
    st.caption("Estudio cuantitativo sobre estrategias de precios, engagement de usuarios y tendencias de consumo.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Simulador de Impacto Financiero
    st.markdown("""
    <div class="simulation-box">
        <h3>📈 Simulador de Impacto Financiero: Ajuste de Precios Globales</h3>
        <p>Mueve el control para simular un aumento de precios (inflación) o una estrategia de descuentos. Mira en tiempo real cómo cambiaría el costo promedio del catálogo y cuántos productos pasarían a ser considerados de gama alta.</p>
    </div>
    """, unsafe_allow_html=True)
    
    cambio_precio = st.slider("Aumentar o disminuir precios de forma simulada (%)", -50, 100, 0, step=5, key="pricing_simulator")
    factor_ajuste = 1 + (cambio_precio / 100)
    
    precio_original_promedio = filtered_df["price_usd"].mean() if not filtered_df.empty else 0
    precio_simulado_promedio = precio_original_promedio * factor_ajuste
    productos_lujo_simulados = len(filtered_df[(filtered_df["price_usd"] * factor_ajuste) > 100]) if not filtered_df.empty else 0
    porcentaje_lujo = (productos_lujo_simulados / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    impacto_teorico = "Estable" if cambio_precio <= 0 else ("Riesgo Ligero" if cambio_precio <= 20 else "Alto Riesgo de Caída")

    
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    
    with sim_col1:
        st.markdown(f"""
        <div class="custom-metric-card">
            <span class="custom-metric-label">Precio Promedio Simulado</span>
            <span class="custom-metric-value">${precio_simulado_promedio:.2f}</span>
            <span class="custom-metric-delta">{cambio_precio}% vs Actual</span>
        </div>
        """, unsafe_allow_html=True)
        
    with sim_col2:
        st.markdown(f"""
        <div class="custom-metric-card">
            <span class="custom-metric-label">Productos que pasarían a valer más de $100</span>
            <span class="custom-metric-value">{productos_lujo_simulados:,}</span>
            <span class="custom-metric-delta">{porcentaje_lujo:.1f}% del catálogo</span>
        </div>
        """, unsafe_allow_html=True)
        
    with sim_col3:
        st.markdown(f"""
        <div class="custom-metric-card">
            <span class="custom-metric-label">Reacción estimada de los clientes</span>
            <span class="custom-metric-value">{impacto_teorico}</span>
            <span class="custom-metric-delta">Predicción inferencial</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # Tarjetas KPI Fijas
    k1, k2, k3, k4 = st.columns(4)
    unique_products = filtered_df["product_id"].nunique() if "product_id" in filtered_df.columns else len(filtered_df)
    avg_rating = filtered_df["review_rating"].mean() if not filtered_df.empty else 0
    total_validos = len(filtered_df[filtered_df["estado_recomendacion"] != "No Especificado"])
    recommendation_rate = (len(filtered_df[filtered_df["estado_recomendacion"] == "Recomendado"]) / total_validos) * 100 if total_validos > 0 else 0

    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Muestra de Productos</div><div class="kpi-value">{unique_products:,}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Calificación Promedio</div><div class="kpi-value">{avg_rating:.2f}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Tasa de Recomendación</div><div class="kpi-value">{recommendation_rate:.1f}%</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Precio Promedio Real</div><div class="kpi-value">${precio_original_promedio:.2f}</div></div>', unsafe_allow_html=True)

    # Gráficos Fila 1
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Precio Promedio por Calificación")
        if len(filtered_df) > 0:
            precio_grouped = filtered_df.groupby("review_rating")["price_usd"].mean().reset_index()
            precio_grouped["price_usd"] = precio_grouped["price_usd"] * factor_ajuste
            precio_grouped = precio_grouped[precio_grouped["review_rating"].isin([1.0, 2.0, 3.0, 4.0, 5.0])]
            precio_grouped["Calificación"] = precio_grouped["review_rating"].astype(int).astype(str) + " ★"
            fig = px.bar(precio_grouped, x="Calificación", y="price_usd", color_discrete_sequence=["#121212"], text=precio_grouped["price_usd"].apply(lambda x: f"${x:.2f}"))
            fig.update_traces(textposition='outside', textfont=dict(color='#000000', weight="bold"))
            fig.update_layout(**layout_charts_editorial)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight"><p class="insight-text">💰 El precio presenta una influencia limitada sobre las calificaciones, lo que sugiere que la satisfacción depende más de la experiencia percibida que del costo del producto.</p></div>', unsafe_allow_html=True)

    with c2:
        st.subheader("Tendencia de Recomendaciones")
        if len(filtered_df) > 0:
            rec_grouped = filtered_df.groupby("estado_recomendacion").size().reset_index(name="Total")
            rec_grouped = rec_grouped[rec_grouped["estado_recomendacion"] != "No Especificado"]
            total_registros = rec_grouped["Total"].sum()
            rec_grouped["Porcentaje"] = (rec_grouped["Total"] / total_registros) * 100 if total_registros > 0 else 0
            
            fig2 = px.bar(rec_grouped, x="estado_recomendacion", y="Porcentaje", color="estado_recomendacion", color_discrete_map={"Recomendado": "#121212", "No Recomendado": "#a1a1aa"}, text=rec_grouped["Porcentaje"].apply(lambda x: f"{x:.1f}%"))
            fig2.update_traces(textposition='inside', textfont=dict(size=13, color='#ffffff', weight='bold'))
            
            fig2.update_layout(**layout_charts_editorial)
            fig2.update_layout(yaxis_range=[0, 110], showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="insight"><p class="insight-text">🗣️ La mayoría de usuarios recomienda los productos analizados, reflejando altos niveles de satisfacción y confianza en la categoría skincare.</p></div>', unsafe_allow_html=True)

    # Gráficos Fila 2
    st.markdown("<br><br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Productos que Impulsan el Engagement")
        if len(filtered_df) > 0:
            engagement = filtered_df.groupby("product_name")["loves_count"].max().sort_values(ascending=False).head(10).reset_index()
            engagement["short_name"] = engagement["product_name"].apply(lambda x: x[:25] + "..." if len(x) > 25 else x)
            fig3 = px.bar(engagement.sort_values("loves_count"), x="loves_count", y="short_name", orientation="h", color_discrete_sequence=["#121212"], text="loves_count")
            fig3.update_traces(texttemplate='%{text:,.0f} ❤️', textposition='inside', textfont=dict(color='#ffffff', weight='bold', size=11))
            
            fig3.update_layout(**layout_charts_editorial)
            fig3.update_layout(xaxis_tickformat=",.0f")
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<div class="insight"><p class="insight-text">📱 El análisis muestra que una pequeña cantidad de productos concentra la mayor parte de la interacción de los usuarios, evidenciando la presencia de artículos altamente populares que dominan la visibilidad y el engagement dentro de la plataforma.</p></div>', unsafe_allow_html=True)

    with c4:
        st.subheader("Crecimiento de Reviews en el Tiempo")
        if len(filtered_df) > 0:
            temporal = filtered_df.groupby("year").size().reset_index(name="Total Reseñas")
            fig4 = px.area(temporal, x="year", y="Total Reseñas", markers=True)
            fig4.update_traces(line=dict(color="#121212", width=3), fillcolor="rgba(0,0,0,0.04)", marker=dict(symbol="star", size=10, color="#000000"))
            fig4.update_layout(**layout_charts_editorial)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown('<div class="insight"><p class="insight-text">📈 La evolución temporal de las reseñas evidencia un crecimiento sostenido de la actividad digital después de 2018, alcanzando sus niveles más altos entre 2019 y 2021 como resultado de una mayor participación de los consumidores en plataformas online.</p></div>', unsafe_allow_html=True)

    # Conclusiones finales fijas
    st.markdown("<br><br><br><h2 style='text-align:center;'>Hallazgos Principales del Análisis de Datos</h2>", unsafe_allow_html=True)
    x_box1, x_box2 = st.columns(2)
    with x_box1:
        st.markdown('<div class="premium-conclusion-box"><h4>💄 1. El Precio Tiene Baja Influencia en la Satisfacción</h4><p>El análisis evidencia una correlación prácticamente nula entre el precio y las calificaciones de los productos. Esto sugiere que los consumidores no necesariamente perciben mayor satisfacción en productos más costosos, lo que indica que factors como la experiencia de uso, la reputación de marca o la efectividad percibida podrían tener un mayor peso en la valoración final.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="premium-conclusion-box" style="margin-top:20px;"><h4>🚀 2. El Engagement se Concentra en un Grupo Reducido de Productos</h4><p>La distribución de la métrica loves_count muestra una alta concentración de interacción en pocos productos. Esto indica que ciertos artículos funcionan como productos altamente virales o representativos dentro del ecosistema Sephora, acumulando gran parte de la atención y popularidad de los usuarios.</p></div>', unsafe_allow_html=True)
    with x_box2:
        st.markdown('<div class="premium-conclusion-box"><h4>📈 3. El Crecimiento de Reviews Aumentó Fuertemente Después de 2018</h4><p>La evolución temporal de las reseñas evidencia un crecimiento significativo de la actividad digital a partir de 2018, alcanzando picos importantes entre 2019 y 2021. Este comportamiento refleja una mayor participación de los usuarios en plataformas digitales y un incremento del contenido generado por consumidores.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="premium-conclusion-box" style="margin-top:20px;"><h4>💖 4. La Tasa de Recomendación Refleja Alta Satisfacción General</h4><p>Más del 84% de los usuarios recomienda los productos analizados. Este resultado sugiere altos niveles de satisfacción dentro de la categoría skincare y refuerza la percepción positiva de los productos disponibles en la plataforma.</p></div>', unsafe_allow_html=True)


# ======================================================
# PÁGINA 2: ARQUETIPOS DE CLIENTA
# ======================================================
if menu == "Perfil de la Clienta":

    st.title("Perfiles de Consumidor: Tono y Estilo")
    st.caption("Segmentación inteligente basada en los perfiles físicos reales de la base de datos.")

    st.markdown(
        """
        <div style="background:#121214; padding:30px; border-radius:12px; margin-bottom:35px; box-shadow:0 10px 30px rgba(0,0,0,0.15);">
            <div style="font-size:30px; font-weight:800; font-family:'Playfair Display', serif; color:#FFFFFF; margin-bottom:15px; line-height:1.2;">
                👤 Segmentación Inteligente de Consumidores
            </div>
            <div style="font-size:16px; color:#d4d4d8; line-height:1.7;">
                Explora perfiles de consumidor según tono de piel, preferencias y comportamiento dentro del catálogo Sephora.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    profiles = [
        {"name": "Subtonos Claros", "label": "Piel Blanca", "image": "clara.jpg", "tones": ['fair', 'light', 'porcelain'], "desc": "Este perfil suele buscar productos con alta protección UV y fórmulas enfocadas en mitigar rojeces y aportar luminosidad."},
        {"name": "Subtonos Neutros", "label": "Piel Morena", "image": "morena.jpg", "tones": ['medium', 'olive', 'tan'], "desc": "Consumidor enfocado en mantener el balance de hidratación, con predilección por acabados naturales que eviten tonos opacos."},
        {"name": "Subtonos Oscuros", "label": "Piel Oscura", "image": "oscura.jpg", "tones": ['dark', 'deep', 'ebony'], "desc": "Perfil con alta lealtad a marcas inclusivas, priorizando la hidratación ultra-profunda y fórmulas con alta concentración de activos."}
    ]

    if "current_profile" not in st.session_state:
        st.session_state.current_profile = None

    # Columnas para los perfiles de piel (Mantenidas dentro de la Página 2)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("clara.jpg", use_container_width=True)
        if st.button("Analizar Piel Blanca"):
            st.session_state.current_profile = profiles[0]

    with col2:
        st.image("morena.jpg", use_container_width=True)
        if st.button("Analizar Piel Morena"):
            st.session_state.current_profile = profiles[1]

    with col3:
        st.image("oscura.jpg", use_container_width=True)
        if st.button("Analizar Piel Oscura"):
            st.session_state.current_profile = profiles[2]

    if st.session_state.current_profile:
        sel = st.session_state.current_profile
        st.markdown(f"<br><h3 style='text-align:center;'>Ficha de Inteligencia de Mercado: {sel['label']}</h3>", unsafe_allow_html=True)
        st.markdown("---")
            
        mask = df["skin_tone"].str.lower().str.contains('|'.join(sel["tones"]), na=False) if "skin_tone" in df.columns else pd.Series(True, index=df.index)
        p_df = df[mask]
            
        if not p_df.empty:
            st.markdown(
                f'''
                <div class="kpi-card" style="margin-bottom:25px;">
                    <div style="color:#FFFFFF; font-size:2rem; font-weight:800; font-family:'Montserrat', sans-serif; margin-bottom:15px;">
                        📋 Perfil del Comprador
                    </div>
                    <div style="color:#d4d4d8; font-size:1rem; line-height:1.7;">
                        {sel["desc"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
            
            c_hab1, c_hab2, c_hab3 = st.columns(3)
            with c_hab1: 
                prod_mode = p_df["product_name"].mode()[0] if not p_df["product_name"].empty else "No disponible"
                st.markdown(f'<div class="kpi-card"><div class="kpi-title">🏆 Producto Más Reseñado</div><div style="font-size:0.95rem; font-weight:700; margin-top:15px; color:#ffffff !important;">{prod_mode}</div></div>', unsafe_allow_html=True)
            with c_hab2: 
                st.markdown(f'<div class="kpi-card"><div class="kpi-title">💰 Gasto Promedio por Artículo</div><div class="kpi-value">${p_df["price_usd"].mean():.2f}</div></div>', unsafe_allow_html=True)
            with c_hab3: 
                st.markdown(f'<div class="kpi-card"><div class="kpi-title">⭐ Satisfacción General (Rating)</div><div class="kpi-value">{p_df["review_rating"].mean():.2f} ★</div></div>', unsafe_allow_html=True)
                    
            st.markdown("<br><br>", unsafe_allow_html=True)
            c_det1, c_det2 = st.columns([1.6, 1])
                    
            with c_det1:
                st.subheader("🧬 Distribución Real del Tipo de Piel")
                if "skin_type" in p_df.columns:
                    piel_df = p_df["skin_type"].dropna().value_counts().reset_index(name="Cantidad")
                    piel_df.columns = ["Tipo de Piel", "Cantidad"]
                    fig_pie = px.pie(piel_df, values="Cantidad", names="Tipo de Piel", color_discrete_sequence=["#121212", "#4b5563", "#71717a", "#d4d4d8"])
                    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#000000", family="Montserrat"), height=280)
                    st.plotly_chart(fig_pie, use_container_width=True)
                        
            with c_det2:
                st.subheader("🏢 Top 3 Marcas de Preferencia")
                if "brand_name" in p_df.columns:
                    top_marcas = p_df["brand_name"].value_counts().head(3).index.tolist()
                    for i, marca in enumerate(top_marcas):
                        st.markdown(f'<div class="kpi-card" style="margin-bottom:10px; padding: 15px;"><span style="font-weight:800; color:#ffffff !important;"># {i+1}</span> <span style="margin-left:10px; color:#e4e4e7 !important; font-weight:600;">{marca}</span></div>', unsafe_allow_html=True)


# ======================================================
# PÁGINA 3: SALUD DE MARCA
# ======================================================
elif menu == "Salud de Marca":

    st.title("📊 Análisis de Reputación y Sentimiento de Marca")
    st.caption("Minería de texto y procesamiento matemático de opiniones y lealtad del cliente.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Todo este bloque de gráficos y métricas ahora está correctamente indentado bajo Salud de Marca
    m1, m2, m3 = st.columns(3)
    total_recs = len(df[df["estado_recomendacion"] == "Recomendado"])
    tasa_global = (total_recs / len(df) * 100) if len(df) > 0 else 0
        
    with m1: 
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">💖 Tasa de Aceptación Global</div><div class="kpi-value">{tasa_global:.1f}%</div></div>', unsafe_allow_html=True)
    with m2: 
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">💬 Opiniones Auditadas</div><div class="kpi-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    with m3: 
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">💡 Utilidad de Reseña (Helpfulness)</div><div class="kpi-value">{df["helpfulness"].mean():.2f}</div></div>', unsafe_allow_html=True)
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_graph, col_explorer = st.columns([4, 3])
        
    with col_graph:
        st.subheader("⭐ Distribución del Scoring de Satisfacción")
        stars_df = df["review_rating"].value_counts().reset_index()
        stars_df.columns = ["Estrellas", "Reviews"]
        stars_df = stars_df[stars_df["Estrellas"].isin([1.0, 2.0, 3.0, 4.0, 5.0])].sort_values("Estrellas")
        stars_df["Estrellas"] = stars_df["Estrellas"].astype(int).astype(str) + " ★"
        fig_stars = px.bar(stars_df, x="Estrellas", y="Reviews", color_discrete_sequence=["#121212"], text="Reviews")
        fig_stars.update_traces(textposition='outside', textfont=dict(color='#000000', weight="bold"))
        fig_stars.update_layout(**layout_charts_editorial)
        st.plotly_chart(fig_stars, use_container_width=True)
            
    with col_explorer:
        st.subheader("🔍 Explorador Temático de Palabras Clave")
        keywords_list = ["piel", "hidratación", "brillo", "suave", "textura", "limpieza", "acné", "absorción", "fresco", "crema"]
        selected_word = st.selectbox("Selecciona un concepto para auditar:", keywords_list)
        mask_word = df["review_text"].str.lower().str.contains(selected_word, na=False) | df["review_title"].str.lower().str.contains(selected_word, na=False)
        word_df = df[mask_word]
        
        if not word_df.empty:
            st.markdown(f'<div class="kpi-card" style="margin-bottom:10px;"><div class="kpi-title">🏆 Producto Líder</div><div style="font-weight:700; font-size:0.9rem; margin-top:5px; color:#ffffff !important;">{word_df["product_name"].mode()[0]}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">💓 Sentimiento Positivo</div><div style="color:#ffffff !important; font-weight:800; font-size:1.6rem; margin-top:5px;">{(len(word_df[word_df["estado_recomendacion"]=="Recomendado"])/len(word_df)*100):.1f}%</div></div>', unsafe_allow_html=True)

    # Polos sentimentales
    st.markdown("<br><br><hr><br>", unsafe_allow_html=True)
    st.subheader("🔥 Comparación de los Polos Sentimentales del Catálogo")
    col_love, col_hate = st.columns(2)
        
    top_loved = df[(df["review_rating"] == 5.0)]["product_name"].mode()[0]
    worst_product = productos_criticos.sort_values("rating_promedio", ascending=True).iloc[0]["product_name"]
        
    with col_love:
        st.markdown(f'<div class="kpi-card" style="border-top-color:#121212 !important;"><h3>😍 El Producto Más Amado</h3><div style="font-weight:600; margin-top:10px; min-height:50px; color:#ffffff !important;">{top_loved}</div></div>', unsafe_allow_html=True)
        data_best = df[df["product_name"] == top_loved].groupby("estado_recomendacion").size().reset_index(name="Total")
        fig_best = px.bar(data_best, x="Total", y="estado_recomendacion", orientation="h", color="estado_recomendacion", color_discrete_map={"Recomendado": "#121212", "No Recomendado": "#a1a1aa"})
        fig_best.update_layout(**layout_charts_editorial)
        fig_best.update_layout(xaxis=dict(visible=False), yaxis=dict(title=""), showlegend=False, height=140)
        st.plotly_chart(fig_best, use_container_width=True)
        
    with col_hate:
        st.markdown(f'<div class="kpi-card" style="border-top-color:#71717a !important;"><h3>😡 El Producto Más Despreciado</h3><div style="font-weight:600; margin-top:10px; min-height:50px; color:#ffffff !important;">{worst_product}</div></div>', unsafe_allow_html=True)
        data_worst = df[df["product_name"] == worst_product].groupby("estado_recomendacion").size().reset_index(name="Total")
        fig_worst = px.bar(data_worst, x="Total", y="estado_recomendacion", orientation="h", color="estado_recomendacion", color_discrete_map={"Recomendado": "#a1a1aa", "No Recomendado": "#121212"})
        fig_worst.update_layout(**layout_charts_editorial)
        fig_worst.update_layout(xaxis=dict(visible=False), yaxis=dict(title=""), showlegend=False, height=140)
        st.plotly_chart(fig_worst, use_container_width=True)

# ======================================================
# PIE DE PÁGINA GLOBAL EDITORIAL
# ======================================================
st.markdown("""
<div class="footer">
Sephora Beauty Database Analytics — Data Portfolio Project - Nicol Escobar
</div>
""", unsafe_allow_html=True)