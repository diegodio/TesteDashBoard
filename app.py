import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURAÇÃO DA PÁGINA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Relatório de Tráfego Pago",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS CUSTOMIZADO — TEMA ESCURO PROFISSIONAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
    /* === RESET & BASE === */
    .stApp {
        background-color: #0a0e1a;
        color: #e2e8f0;
    }
    
    /* Header area */
    header[data-testid="stHeader"] {
        background-color: #0a0e1a;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #0f172a;
        padding: 4px 8px;
        border-radius: 12px;
        border: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #64748b;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.3px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #818cf820 !important;
        color: #818cf8 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #818cf8 !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #ffffff12;
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="stMetric"] label {
        color: #8892b0 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Markdown text */
    .stMarkdown p, .stMarkdown li {
        color: #cbd5e1;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    
    /* Divider */
    hr {
        border-color: #1e293b !important;
    }

    /* Custom KPI box */
    .kpi-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #ffffff12;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .kpi-label {
        font-size: 11px;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .kpi-sub {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }
    
    /* Section header */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 24px 0 16px 0;
        font-size: 16px;
        font-weight: 700;
        color: #e2e8f0;
    }
    .section-bar {
        width: 4px;
        height: 20px;
        border-radius: 2px;
        display: inline-block;
    }
    
    /* Observation card */
    .obs-card {
        background: #ffffff06;
        border-left: 3px solid #818cf860;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    .obs-num {
        color: #818cf8;
        font-weight: 800;
        font-size: 12px;
        flex-shrink: 0;
        min-width: 24px;
    }
    .obs-text {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.65;
    }
    
    /* Action card */
    .action-card {
        background: #34d39908;
        border: 1px solid #34d39920;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    .action-num {
        width: 24px;
        height: 24px;
        border-radius: 6px;
        border: 2px solid #34d39960;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        color: #34d399;
        flex-shrink: 0;
    }
    .action-text {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.65;
    }

    /* Status badges */
    .badge-ativa {
        background: #0d3320;
        color: #34d399;
        border: 1px solid #166534;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-pausada {
        background: #3b1a1a;
        color: #f87171;
        border: 1px solid #7f1d1d;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-teste {
        background: #2d2305;
        color: #fbbf24;
        border: 1px solid #713f12;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* Meta card */
    .meta-card {
        background: #ffffff06;
        border: 1px solid #ffffff08;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .meta-card-label {
        font-size: 10px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .meta-card-atual {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 4px;
    }
    .meta-card-target {
        font-size: 16px;
        color: #fbbf24;
        font-weight: 800;
        margin-top: 4px;
    }

    /* Highlight box */
    .highlight-box {
        background: #fbbf2410;
        border: 1px solid #fbbf2430;
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 12px;
    }
    .highlight-box strong {
        color: #fbbf24;
    }

    /* Creative ranking */
    .creative-rank {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        flex-wrap: wrap;
    }
    .creative-rank-1 {
        background: linear-gradient(135deg, #1e1b4b40, #0f172a);
        border: 1px solid #4f46e540;
    }
    .creative-rank-other {
        background: #ffffff04;
        border: 1px solid #ffffff08;
    }
    .rank-badge {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 900;
        color: #0a0e1a;
        flex-shrink: 0;
    }
    
    /* Report header */
    .report-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border-bottom: 1px solid #312e81;
        border-radius: 16px;
        padding: 32px 28px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .report-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 70% 20%, #4f46e520 0%, transparent 50%);
    }
    .header-tag {
        font-size: 11px;
        color: #818cf8;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        margin-bottom: 6px;
        position: relative;
    }
    .header-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #e2e8f0;
        position: relative;
    }
    .header-right {
        text-align: right;
        position: relative;
    }
    .header-period {
        font-size: 14px;
        font-weight: 700;
        color: #c7d2fe;
    }
    .header-gestor {
        font-size: 11px;
        color: #64748b;
        margin-top: 4px;
    }

    /* Footer */
    .report-footer {
        text-align: center;
        padding: 24px 0 8px;
        border-top: 1px solid #1e293b;
        margin-top: 24px;
    }
    .footer-main {
        font-size: 11px;
        color: #475569;
    }
    .footer-sub {
        font-size: 10px;
        color: #334155;
        margin-top: 4px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DADOS DE EXEMPLO (substitua pelos dados reais do cliente)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATA = {
    "cliente": "Nome do Cliente",
    "periodo": "01/05/2026 a 31/05/2026",
    "gestor": "Seu Nome Aqui",
    # Investimento
    "investimento_total": 12_450.00,
    "investimento_meta": 8_200.00,
    "investimento_google": 4_250.00,
    # Resultados
    "leads": 847,
    "vendas": 38,
    "faturamento": 76_000.00,
}

META_ADS = {
    "impressoes": 385_000,
    "alcance": 142_000,
    "cliques": 9_800,
    "ctr": 2.54,
    "cpc": 0.84,
    "cpm": 21.30,
    "cpl": 11.82,
    "leads": 694,
    "frequencia": 2.71,
}

META_CAMPANHAS = pd.DataFrame([
    {"Campanha": "[CONVERSÃO] Captação - Público Frio - Interesses", "Objetivo": "Leads", "Investido": 3200, "Leads": 285, "CPL": 11.23, "CTR": 2.8, "Status": "ativa"},
    {"Campanha": "[CONVERSÃO] Captação - Lookalike 1%", "Objetivo": "Leads", "Investido": 2100, "Leads": 198, "CPL": 10.61, "CTR": 3.1, "Status": "ativa"},
    {"Campanha": "[CONVERSÃO] Remarketing - Engajamento 7d", "Objetivo": "Leads", "Investido": 1500, "Leads": 142, "CPL": 10.56, "CTR": 4.2, "Status": "ativa"},
    {"Campanha": "[CONVERSÃO] Remarketing - Visitou Site 30d", "Objetivo": "Leads", "Investido": 900, "Leads": 52, "CPL": 17.31, "CTR": 3.5, "Status": "pausada"},
    {"Campanha": "[TRÁFEGO] Aquecimento - Vídeo View", "Objetivo": "Views", "Investido": 500, "Leads": 17, "CPL": 29.41, "CTR": 1.9, "Status": "ativa"},
])

GOOGLE_ADS = {
    "impressoes": 98_000,
    "cliques": 5_200,
    "ctr": 5.31,
    "cpc": 0.82,
    "conversoes": 153,
    "taxa_conversao": 2.94,
    "cpl": 27.78,
}

GOOGLE_CAMPANHAS = pd.DataFrame([
    {"Campanha": "[SEARCH] Marca", "Investido": 800, "Cliques": 1200, "Conversões": 48, "CPL": 16.67, "CTR": 12.5, "Status": "ativa"},
    {"Campanha": "[SEARCH] Genérica - Produto", "Investido": 1800, "Cliques": 2100, "Conversões": 62, "CPL": 29.03, "CTR": 4.2, "Status": "ativa"},
    {"Campanha": "[SEARCH] Concorrentes", "Investido": 650, "Cliques": 800, "Conversões": 18, "CPL": 36.11, "CTR": 3.8, "Status": "ativa"},
    {"Campanha": "[DISPLAY] Remarketing", "Investido": 600, "Cliques": 700, "Conversões": 15, "CPL": 40.00, "CTR": 0.8, "Status": "ativa"},
    {"Campanha": "[PMAX] Performance Max", "Investido": 400, "Cliques": 400, "Conversões": 10, "CPL": 40.00, "CTR": 2.1, "Status": "teste"},
])

HISTORICO = pd.DataFrame([
    {"Mês": "Dez", "Investimento": 8500, "Leads": 520, "Vendas": 22, "Faturamento": 44000},
    {"Mês": "Jan", "Investimento": 9200, "Leads": 580, "Vendas": 25, "Faturamento": 50000},
    {"Mês": "Fev", "Investimento": 10000, "Leads": 640, "Vendas": 28, "Faturamento": 56000},
    {"Mês": "Mar", "Investimento": 10800, "Leads": 710, "Vendas": 31, "Faturamento": 62000},
    {"Mês": "Abr", "Investimento": 11500, "Leads": 780, "Vendas": 35, "Faturamento": 70000},
    {"Mês": "Mai", "Investimento": 12450, "Leads": 847, "Vendas": 38, "Faturamento": 76000},
])

TOP_CRIATIVOS = [
    {"nome": "Vídeo Depoimento - Maria", "ctr": 4.8, "cpl": 8.20, "leads": 142, "formato": "Vídeo 1:1"},
    {"nome": "Carrossel - Antes e Depois", "ctr": 3.9, "cpl": 9.50, "leads": 118, "formato": "Carrossel"},
    {"nome": "Estático - Oferta Direta", "ctr": 3.2, "cpl": 11.80, "leads": 95, "formato": "Imagem 1:1"},
]

OBSERVACOES = [
    "CPL geral caiu 8% em relação ao mês anterior — resultado da otimização nos públicos lookalike.",
    "Campanha de remarketing de visitantes do site (30d) pausada por CPL acima do aceitável. Vamos testar novo criativo antes de reativar.",
    "Vídeo de depoimento continua sendo o criativo com melhor performance. Recomendo produzir mais 2 depoimentos este mês.",
    "Google Ads: campanha de marca segue com excelente CPA. Campanha PMAX ainda em fase de aprendizado.",
]

PROXIMOS_PASSOS = [
    "Escalar orçamento das campanhas com CPL abaixo de R$ 12,00 em 15%.",
    "Criar 3 novos criativos de vídeo baseados nos depoimentos com melhor performance.",
    "Testar novo público lookalike baseado em compradores (não apenas leads).",
    "Implementar tracking de valor de conversão no Google Ads para otimizar ROAS.",
    "Reunião de alinhamento na próxima terça para definir metas do próximo trimestre.",
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNÇÕES AUXILIARES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_num(v):
    return f"{v:,.0f}".replace(",", ".")

def fmt_pct(v):
    return f"{v:.2f}%".replace(".", ",")

def status_badge(s):
    cls = f"badge-{s}"
    return f'<span class="{cls}">{s}</span>'

def plotly_dark_layout(fig, height=320):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        margin=dict(l=20, r=20, t=30, b=20),
        height=height,
        xaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
        legend=dict(font=dict(color="#94a3b8", size=10)),
        hoverlabel=dict(bgcolor="#1e293b", font_color="#e2e8f0", bordercolor="#333"),
    )
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MÉTRICAS DERIVADAS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

d = DATA
roas = d["faturamento"] / d["investimento_total"]
cpl = d["investimento_total"] / d["leads"]
cpa = d["investimento_total"] / d["vendas"]
taxa_conv = (d["vendas"] / d["leads"]) * 100
ticket_medio = d["faturamento"] / d["vendas"]
lucro_bruto = d["faturamento"] - d["investimento_total"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown(f"""
<div class="report-header">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
        <div>
            <div class="header-tag">📊 Relatório de Tráfego Pago</div>
            <div class="header-title">{d['cliente']}</div>
        </div>
        <div class="header-right">
            <div style="font-size:12px; color:#94a3b8;">Período</div>
            <div class="header-period">{d['periodo']}</div>
            <div class="header-gestor">Gestor: {d['gestor']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TABS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tab_visao, tab_meta, tab_google, tab_criativos, tab_plano = st.tabs([
    "📈 Visão Geral",
    "📱 Meta Ads",
    "🔍 Google Ads",
    "🎨 Criativos",
    "🎯 Plano de Ação",
])


# ═══════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ═══════════════════════════════════════════════════════════
with tab_visao:

    # KPIs principais
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Investimento Total", fmt_brl(d["investimento_total"]))
    c2.metric("🎯 Leads Gerados", fmt_num(d["leads"]), f"CPL: {fmt_brl(cpl)}")
    c3.metric("🛒 Vendas", fmt_num(d["vendas"]), f"Conv: {fmt_pct(taxa_conv)}")
    c4.metric("📈 Faturamento", fmt_brl(d["faturamento"]), f"ROAS: {roas:.2f}x")

    st.markdown("")

    # Métricas secundárias
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Métricas Secundárias</div>', unsafe_allow_html=True)

    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
    for col, label, val in [
        (sc1, "CPA", fmt_brl(cpa)),
        (sc2, "CPL Médio", fmt_brl(cpl)),
        (sc3, "ROAS", f"{roas:.2f}x"),
        (sc4, "Conv. Lead→Venda", fmt_pct(taxa_conv)),
        (sc5, "Ticket Médio", fmt_brl(ticket_medio)),
        (sc6, "Lucro Bruto", fmt_brl(lucro_bruto)),
    ]:
        col.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:#e2e8f0;">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Evolução mensal — gráficos
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#34d399;"></span> Evolução Mensal</div>', unsafe_allow_html=True)

    gc1, gc2, gc3 = st.columns(3)

    with gc1:
        fig = go.Figure(go.Bar(
            x=HISTORICO["Mês"], y=HISTORICO["Leads"],
            marker=dict(color="#34d399", cornerradius=6),
            text=HISTORICO["Leads"], textposition="outside",
            textfont=dict(color="#94a3b8", size=10),
        ))
        fig.update_layout(title=dict(text="Leads", font=dict(size=13, color="#64748b")))
        plotly_dark_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    with gc2:
        fig = go.Figure(go.Bar(
            x=HISTORICO["Mês"], y=HISTORICO["Vendas"],
            marker=dict(color="#818cf8", cornerradius=6),
            text=HISTORICO["Vendas"], textposition="outside",
            textfont=dict(color="#94a3b8", size=10),
        ))
        fig.update_layout(title=dict(text="Vendas", font=dict(size=13, color="#64748b")))
        plotly_dark_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    with gc3:
        fig = go.Figure(go.Bar(
            x=HISTORICO["Mês"], y=HISTORICO["Investimento"],
            marker=dict(color="#f59e0b", cornerradius=6),
            text=[f"R${v/1000:.1f}k" for v in HISTORICO["Investimento"]],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=10),
        ))
        fig.update_layout(title=dict(text="Investimento", font=dict(size=13, color="#64748b")))
        plotly_dark_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Distribuição de investimento
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#f59e0b;"></span> Distribuição de Investimento</div>', unsafe_allow_html=True)

    di1, di2 = st.columns(2)
    meta_pct = d["investimento_meta"] / d["investimento_total"] * 100
    google_pct = d["investimento_google"] / d["investimento_total"] * 100

    with di1:
        fig = go.Figure(go.Pie(
            labels=["Meta Ads", "Google Ads"],
            values=[d["investimento_meta"], d["investimento_google"]],
            marker=dict(colors=["#818cf8", "#34d399"]),
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(color="#e2e8f0", size=12),
        ))
        fig.update_layout(showlegend=False)
        plotly_dark_layout(fig, height=280)
        st.plotly_chart(fig, use_container_width=True)

    with di2:
        st.markdown("")
        st.markdown("")
        st.markdown(f"""
        <div style="padding:20px;">
            <div style="margin-bottom:20px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="color:#818cf8;font-weight:700;">📱 Meta Ads</span>
                    <span style="color:#94a3b8;">{fmt_brl(d['investimento_meta'])} ({meta_pct:.0f}%)</span>
                </div>
                <div style="width:100%;height:8px;background:#ffffff10;border-radius:4px;">
                    <div style="width:{meta_pct}%;height:100%;background:#818cf8;border-radius:4px;"></div>
                </div>
            </div>
            <div>
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="color:#34d399;font-weight:700;">🔍 Google Ads</span>
                    <span style="color:#94a3b8;">{fmt_brl(d['investimento_google'])} ({google_pct:.0f}%)</span>
                </div>
                <div style="width:100%;height:8px;background:#ffffff10;border-radius:4px;">
                    <div style="width:{google_pct}%;height:100%;background:#34d399;border-radius:4px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 2 — META ADS
# ═══════════════════════════════════════════════════════════
with tab_meta:

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📱 Impressões", fmt_num(META_ADS["impressoes"]))
    m2.metric("👥 Alcance", fmt_num(META_ADS["alcance"]), f"Freq: {META_ADS['frequencia']:.2f}")
    m3.metric("🖱️ Cliques", fmt_num(META_ADS["cliques"]), f"CTR: {fmt_pct(META_ADS['ctr'])}")
    m4.metric("🎯 Leads", fmt_num(META_ADS["leads"]), f"CPL: {fmt_brl(META_ADS['cpl'])}")

    st.markdown("")

    # Métricas de custo
    mc1, mc2, mc3, mc4 = st.columns(4)
    for col, label, val in [
        (mc1, "CPC", fmt_brl(META_ADS["cpc"])),
        (mc2, "CPM", fmt_brl(META_ADS["cpm"])),
        (mc3, "CTR", fmt_pct(META_ADS["ctr"])),
        (mc4, "Frequência", f"{META_ADS['frequencia']:.2f}"),
    ]:
        col.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:#e2e8f0;">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Tabela de campanhas
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Campanhas Meta Ads</div>', unsafe_allow_html=True)

    # Montar tabela HTML para visual mais rico
    rows_html = ""
    for _, r in META_CAMPANHAS.iterrows():
        cpl_color = "#34d399" if r["CPL"] < 12 else ("#fbbf24" if r["CPL"] < 20 else "#f87171")
        rows_html += f"""
        <tr style="border-bottom:1px solid #ffffff08;">
            <td style="padding:12px;font-size:12px;font-weight:600;color:#cbd5e1;max-width:300px;">{r['Campanha']}</td>
            <td style="padding:12px;text-align:right;font-family:monospace;color:#cbd5e1;">{fmt_brl(r['Investido'])}</td>
            <td style="padding:12px;text-align:right;font-weight:700;color:#34d399;">{r['Leads']}</td>
            <td style="padding:12px;text-align:right;color:{cpl_color};font-weight:700;">{fmt_brl(r['CPL'])}</td>
            <td style="padding:12px;text-align:right;color:#cbd5e1;">{fmt_pct(r['CTR'])}</td>
            <td style="padding:12px;text-align:center;">{status_badge(r['Status'])}</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:14px;overflow:hidden;">
        <table style="width:100%;border-collapse:collapse;">
            <thead>
                <tr style="border-bottom:1px solid #1e293b;">
                    <th style="padding:12px;text-align:left;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Campanha</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Investido</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Leads</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">CPL</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">CTR</th>
                    <th style="padding:12px;text-align:center;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Gráfico CPL por campanha
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#a78bfa;"></span> CPL por Campanha</div>', unsafe_allow_html=True)

    fig = go.Figure(go.Bar(
        y=META_CAMPANHAS["Campanha"].str[:40],
        x=META_CAMPANHAS["CPL"],
        orientation="h",
        marker=dict(
            color=["#34d399" if v < 12 else ("#fbbf24" if v < 20 else "#f87171") for v in META_CAMPANHAS["CPL"]],
            cornerradius=4,
        ),
        text=[fmt_brl(v) for v in META_CAMPANHAS["CPL"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=10),
    ))
    plotly_dark_layout(fig, height=250)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — GOOGLE ADS
# ═══════════════════════════════════════════════════════════
with tab_google:

    g1, g2, g3, g4 = st.columns(4)
    g1.metric("🔍 Impressões", fmt_num(GOOGLE_ADS["impressoes"]))
    g2.metric("🖱️ Cliques", fmt_num(GOOGLE_ADS["cliques"]), f"CTR: {fmt_pct(GOOGLE_ADS['ctr'])}")
    g3.metric("💰 CPC Médio", fmt_brl(GOOGLE_ADS["cpc"]))
    g4.metric("🎯 Conversões", fmt_num(GOOGLE_ADS["conversoes"]), f"CPL: {fmt_brl(GOOGLE_ADS['cpl'])}")

    st.markdown("")

    # Tabela de campanhas Google
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#34d399;"></span> Campanhas Google Ads</div>', unsafe_allow_html=True)

    rows_html_g = ""
    for _, r in GOOGLE_CAMPANHAS.iterrows():
        cpl_color = "#34d399" if r["CPL"] < 20 else ("#fbbf24" if r["CPL"] < 35 else "#f87171")
        rows_html_g += f"""
        <tr style="border-bottom:1px solid #ffffff08;">
            <td style="padding:12px;font-size:12px;font-weight:600;color:#cbd5e1;">{r['Campanha']}</td>
            <td style="padding:12px;text-align:right;font-family:monospace;color:#cbd5e1;">{fmt_brl(r['Investido'])}</td>
            <td style="padding:12px;text-align:right;color:#cbd5e1;">{fmt_num(r['Cliques'])}</td>
            <td style="padding:12px;text-align:right;font-weight:700;color:#34d399;">{r['Conversões']}</td>
            <td style="padding:12px;text-align:right;color:{cpl_color};font-weight:700;">{fmt_brl(r['CPL'])}</td>
            <td style="padding:12px;text-align:right;color:#cbd5e1;">{fmt_pct(r['CTR'])}</td>
            <td style="padding:12px;text-align:center;">{status_badge(r['Status'])}</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:14px;overflow:hidden;">
        <table style="width:100%;border-collapse:collapse;">
            <thead>
                <tr style="border-bottom:1px solid #1e293b;">
                    <th style="padding:12px;text-align:left;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Campanha</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Investido</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Cliques</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Conversões</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">CPL</th>
                    <th style="padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">CTR</th>
                    <th style="padding:12px;text-align:center;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Status</th>
                </tr>
            </thead>
            <tbody>{rows_html_g}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Gráfico: Conversões vs Investimento
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#60a5fa;"></span> Conversões vs Investimento por Campanha</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=GOOGLE_CAMPANHAS["Campanha"].str.replace(r"\[.*?\]\s*", "", regex=True),
        y=GOOGLE_CAMPANHAS["Investido"],
        name="Investido (R$)",
        marker=dict(color="#60a5fa80", cornerradius=4),
    ))
    fig.add_trace(go.Bar(
        x=GOOGLE_CAMPANHAS["Campanha"].str.replace(r"\[.*?\]\s*", "", regex=True),
        y=GOOGLE_CAMPANHAS["Conversões"] * 15,  # scale for visibility
        name="Conversões (×15)",
        marker=dict(color="#34d399", cornerradius=4),
    ))
    fig.update_layout(barmode="group")
    plotly_dark_layout(fig, height=300)
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 4 — CRIATIVOS
# ═══════════════════════════════════════════════════════════
with tab_criativos:

    st.markdown('<div class="section-header"><span class="section-bar" style="background:#f59e0b;"></span> Top 3 Criativos do Período</div>', unsafe_allow_html=True)

    for i, c in enumerate(TOP_CRIATIVOS):
        rank_bg = "#fbbf24" if i == 0 else ("#94a3b8" if i == 1 else "#b45309")
        rank_class = "creative-rank-1" if i == 0 else "creative-rank-other"
        st.markdown(f"""
        <div class="creative-rank {rank_class}">
            <div class="rank-badge" style="background:{rank_bg};">{i+1}</div>
            <div style="flex:1 1 200px;min-width:150px;">
                <div style="font-size:15px;font-weight:700;color:#e2e8f0;">{c['nome']}</div>
                <div style="font-size:11px;color:#64748b;margin-top:2px;">{c['formato']}</div>
            </div>
            <div style="display:flex;gap:28px;flex-wrap:wrap;">
                <div style="text-align:center;">
                    <div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:600;">CTR</div>
                    <div style="font-size:18px;font-weight:800;color:#34d399;margin-top:2px;">{fmt_pct(c['ctr'])}</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:600;">CPL</div>
                    <div style="font-size:18px;font-weight:800;color:#818cf8;margin-top:2px;">{fmt_brl(c['cpl'])}</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:600;">Leads</div>
                    <div style="font-size:18px;font-weight:800;color:#fbbf24;margin-top:2px;">{c['leads']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Análise de Criativos</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:20px;">
        <p style="margin:0 0 12px;color:#94a3b8;font-size:13px;line-height:1.7;">
            <strong style="color:#e2e8f0;">Padrão identificado:</strong> Criativos com prova social (depoimentos em vídeo) seguem superando os formatos estáticos em CTR e CPL. O formato vídeo 1:1 com depoimento de cliente performou <span style="color:#34d399;font-weight:700;">50% melhor</span> em CPL comparado ao estático de oferta direta.
        </p>
        <p style="margin:0 0 12px;color:#94a3b8;font-size:13px;line-height:1.7;">
            <strong style="color:#e2e8f0;">Recomendação:</strong> Concentrar a produção de novos criativos em depoimentos curtos (15-30s) e carrosséis de antes/depois. Testar formato Reels com hook nos primeiros 3 segundos.
        </p>
        <div class="highlight-box">
            ⚡ <strong>AÇÃO:</strong> <span style="color:#cbd5e1;">Solicitar ao cliente a gravação de 2-3 novos depoimentos seguindo o roteiro enviado por e-mail em 15/05.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Gráfico comparativo de CTR
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#34d399;"></span> Comparativo de Performance</div>', unsafe_allow_html=True)

    fig = go.Figure()
    nomes = [c["nome"] for c in TOP_CRIATIVOS]
    fig.add_trace(go.Bar(
        x=nomes, y=[c["ctr"] for c in TOP_CRIATIVOS],
        name="CTR (%)", marker=dict(color="#34d399", cornerradius=6),
    ))
    fig.add_trace(go.Bar(
        x=nomes, y=[c["cpl"] for c in TOP_CRIATIVOS],
        name="CPL (R$)", marker=dict(color="#818cf8", cornerradius=6),
    ))
    fig.update_layout(barmode="group")
    plotly_dark_layout(fig, height=280)
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 5 — PLANO DE AÇÃO
# ═══════════════════════════════════════════════════════════
with tab_plano:

    # Observações
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Observações do Gestor</div>', unsafe_allow_html=True)

    obs_html = ""
    for i, obs in enumerate(OBSERVACOES, 1):
        obs_html += f"""
        <div class="obs-card">
            <span class="obs-num">{str(i).zfill(2)}</span>
            <span class="obs-text">{obs}</span>
        </div>"""
    st.markdown(obs_html, unsafe_allow_html=True)

    st.markdown("")

    # Próximos passos
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#34d399;"></span> Próximos Passos</div>', unsafe_allow_html=True)

    act_html = ""
    for i, p in enumerate(PROXIMOS_PASSOS, 1):
        act_html += f"""
        <div class="action-card">
            <div class="action-num">{i}</div>
            <span class="action-text">{p}</span>
        </div>"""
    st.markdown(act_html, unsafe_allow_html=True)

    st.markdown("")

    # Metas próximo período
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#fbbf24;"></span> Metas para o Próximo Período</div>', unsafe_allow_html=True)

    mt1, mt2, mt3, mt4 = st.columns(4)
    metas = [
        (mt1, "💰", "Investimento", fmt_brl(d["investimento_total"]), fmt_brl(14300)),
        (mt2, "🎯", "Leads", fmt_num(d["leads"]), "950+"),
        (mt3, "📉", "CPL Meta Ads", fmt_brl(META_ADS["cpl"]), "< R$ 11,00"),
        (mt4, "🛒", "Vendas", fmt_num(d["vendas"]), "45+"),
    ]
    for col, icon, label, atual, meta in metas:
        col.markdown(f"""
        <div class="meta-card">
            <div style="font-size:24px;margin-bottom:8px;">{icon}</div>
            <div class="meta-card-label">{label}</div>
            <div class="meta-card-atual">Atual: <strong style="color:#e2e8f0;">{atual}</strong></div>
            <div class="meta-card-target">Meta: {meta}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Gráfico de projeção
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#a78bfa;"></span> Tendência de Crescimento</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=HISTORICO["Mês"], y=HISTORICO["Faturamento"],
        mode="lines+markers+text",
        name="Faturamento",
        line=dict(color="#818cf8", width=3),
        marker=dict(size=8, color="#818cf8"),
        text=[f"R${v/1000:.0f}k" for v in HISTORICO["Faturamento"]],
        textposition="top center",
        textfont=dict(color="#94a3b8", size=10),
    ))
    fig.add_trace(go.Scatter(
        x=HISTORICO["Mês"], y=HISTORICO["Investimento"],
        mode="lines+markers+text",
        name="Investimento",
        line=dict(color="#f59e0b", width=2, dash="dot"),
        marker=dict(size=6, color="#f59e0b"),
        text=[f"R${v/1000:.1f}k" for v in HISTORICO["Investimento"]],
        textposition="bottom center",
        textfont=dict(color="#94a3b8", size=9),
    ))
    plotly_dark_layout(fig, height=320)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown(f"""
<div class="report-footer">
    <div class="footer-main">Relatório gerado por {d['gestor']} • Estilo Comunidade Sobral de Tráfego</div>
    <div class="footer-sub">"Coleta → Análise → Ação" — O ciclo que gera resultado.</div>
</div>
""", unsafe_allow_html=True)