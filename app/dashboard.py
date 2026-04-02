import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="The Business Guardian", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CSS Styling für Metriken ---
st.markdown("""
    <style>
    .big-font { font-size: 24px !important; font-weight: bold; }
    .alert-box { background-color: #ff4b4b; padding: 15px; border-radius: 5px; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    macro_path = os.path.join("data", "macro_detection_results.csv")
    if not os.path.exists(macro_path):
        return None
    
    df_macro = pd.read_csv(macro_path)
    df_macro['date'] = pd.to_datetime(df_macro['date'])
    return df_macro

@st.cache_data
def load_rca_data(date_str):
    rca_path = os.path.join("data", f"rca_results_{date_str}.csv")
    if os.path.exists(rca_path):
        return pd.read_csv(rca_path)
    return None

df_macro = load_data()

# --- Main Dashboard ---
st.title("🛡️ The Business Guardian: Command Center")
st.markdown("*Automated Macro-Detection & Multidimensional Root Cause Analysis*")

if df_macro is None:
    st.error("Keine Daten gefunden. Bitte führe zuerst Phase 1 & 2 aus!")
    st.stop()

# --- KPI Row ---
total_revenue = df_macro['revenue'].sum()
anomalies_count = df_macro['is_macro_anomaly'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (90 Days)", f"€ {total_revenue:,.0f}")
col2.metric("Days Analyzed", len(df_macro))
col3.metric("Anomalies Detected", anomalies_count, delta_color="inverse", delta=f"{anomalies_count} Critical Issues")

st.divider()

# --- Visualization: Macro Timeline ---
st.subheader("📈 Macro Level: Revenue Anomaly Detection")
st.markdown("Das System überwacht den Gesamtumsatz bereinigt um Saisonalität. Rote Punkte markieren statistisch signifikante Ausreißer (Z-Score > 3.5).")

# Erstelle den Plot
fig = go.Figure()

# Normale Umsatz-Linie
fig.add_trace(go.Scatter(
    x=df_macro['date'], y=df_macro['revenue'],
    mode='lines', name='Daily Revenue',
    line=dict(color='#2E86C1', width=2)
))

# Anomalien als rote Marker
anomalies = df_macro[df_macro['is_macro_anomaly'] == 1]
fig.add_trace(go.Scatter(
    x=anomalies['date'], y=anomalies['revenue'],
    mode='markers', name='Anomaly Detected',
    marker=dict(color='red', size=12, symbol='x')
))

# Trend-Linie als Orientierung
fig.add_trace(go.Scatter(
    x=df_macro['date'], y=df_macro['trend'],
    mode='lines', name='Trend (STL)',
    line=dict(color='rgba(46, 134, 193, 0.3)', width=2, dash='dash')
))

fig.update_layout(hovermode="x unified", xaxis_title="Date", yaxis_title="Revenue (EUR)", margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# --- Root Cause Analysis Section ---
st.divider()
st.subheader("🔍 Automated Root Cause Analysis (The 'Why')")

if anomalies.empty:
    st.success("Aktuell keine Anomalien zu untersuchen. Alles im grünen Bereich!")
else:
    # Auswahl der Anomalie
    anomaly_dates = anomalies['date'].dt.strftime('%Y-%m-%d').tolist()
    selected_date = st.selectbox("Wähle ein Anomalie-Datum für den Drill-down:", anomaly_dates)
    
    # Lade die zugehörigen RCA Ergebnisse
    df_rca = load_rca_data(selected_date)
    
    if df_rca is not None and not df_rca.empty:
        top_cause = df_rca.iloc[0]
        
        # Simulierter Slack-Alert
        st.markdown(f"""
        <div class="alert-box">
            🚨 SYSTEM ALERT: Starker Umsatzabfall am {selected_date}!<br>
            Wahrscheinlichste Ursache: <b>{top_cause['segment']}</b><br>
            Geschätzter Verlust: <b>€ {top_cause['revenue_impact_eur']:,.2f}</b>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            st.markdown("### Top 5 Fehler-Segmente")
            # Bar Chart für den Impact
            fig_rca = px.bar(
                df_rca.head(5), 
                x='revenue_impact_eur', 
                y='segment', 
                orientation='h',
                title="Revenue Lost by Segment (EUR)",
                color='revenue_impact_eur',
                color_continuous_scale='Reds'
            )
            fig_rca.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_rca, use_container_width=True)
            
        with col_b:
            st.markdown("### Detaillierte Drill-down Metriken")
            # Tabelle formatieren für bessere Lesbarkeit
            display_df = df_rca.head(5)[['segment', 'level', 'expected_cvr', 'actual_cvr', 'revenue_impact_eur']].copy()
            display_df['expected_cvr'] = (display_df['expected_cvr'] * 100).round(2).astype(str) + '%'
            display_df['actual_cvr'] = (display_df['actual_cvr'] * 100).round(2).astype(str) + '%'
            display_df['revenue_impact_eur'] = display_df['revenue_impact_eur'].round(0).astype(int)
            
            st.dataframe(display_df, use_container_width=True)
            
    else:
        st.info("Für dieses Datum liegen noch keine RCA-Ergebnisse vor. Bitte führe Phase 3 aus.")