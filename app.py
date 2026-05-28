import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURAÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="Relatório de Tráfego Pago", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; color: #e2e8f0; }
    header[data-testid="stHeader"] { background-color: #0a0e1a; }
    section[data-testid="stSidebar"] { background-color: #0f172a; }

    .stTabs [data-baseweb="tab-list"] { gap:4px; background-color:#0f172a; padding:4px 8px; border-radius:12px; border:1px solid #1e293b; }
    .stTabs [data-baseweb="tab"] { background-color:transparent; color:#64748b; border-radius:8px; padding:8px 20px; font-weight:700; font-size:13px; }
    .stTabs [aria-selected="true"] { background-color:#818cf820 !important; color:#818cf8 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color:#818cf8 !important; }
    .stTabs [data-baseweb="tab-border"] { display:none; }

    div[data-testid="stMetric"] { background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%); border:1px solid #ffffff12; border-radius:12px; padding:16px 20px; }
    div[data-testid="stMetric"] label { color:#8892b0 !important; font-size:11px !important; text-transform:uppercase; letter-spacing:1.2px; font-weight:600 !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#e2e8f0 !important; font-weight:800 !important; font-size:24px !important; }

    .kpi-box { background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%); border:1px solid #ffffff12; border-radius:12px; padding:20px; text-align:center; }
    .kpi-label { font-size:11px; color:#8892b0; text-transform:uppercase; letter-spacing:1.2px; font-weight:600; margin-bottom:4px; }
    .kpi-value { font-size:26px; font-weight:800; color:#e2e8f0; letter-spacing:-0.5px; }
    .kpi-sub { font-size:12px; color:#64748b; margin-top:4px; }

    .section-header { display:flex; align-items:center; gap:10px; margin:24px 0 16px 0; font-size:16px; font-weight:700; color:#e2e8f0; }
    .section-bar { width:4px; height:20px; border-radius:2px; display:inline-block; }

    .obs-card { background:#ffffff06; border-left:3px solid #818cf860; border-radius:0 10px 10px 0; padding:14px 18px; margin-bottom:10px; display:flex; gap:12px; align-items:flex-start; }
    .obs-num { color:#818cf8; font-weight:800; font-size:12px; flex-shrink:0; min-width:24px; }
    .obs-text { font-size:13px; color:#cbd5e1; line-height:1.65; }

    .action-card { background:#34d39908; border:1px solid #34d39920; border-radius:10px; padding:14px 18px; margin-bottom:10px; display:flex; gap:12px; align-items:flex-start; }
    .action-num { width:24px; height:24px; border-radius:6px; border:2px solid #34d39960; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:800; color:#34d399; flex-shrink:0; }
    .action-text { font-size:13px; color:#cbd5e1; line-height:1.65; }

    .badge-ativa,.badge-Ativa { background:#0d3320; color:#34d399; border:1px solid #166534; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:600; text-transform:uppercase; }
    .badge-pausada,.badge-Pausada { background:#3b1a1a; color:#f87171; border:1px solid #7f1d1d; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:600; text-transform:uppercase; }
    .badge-teste,.badge-Teste { background:#2d2305; color:#fbbf24; border:1px solid #713f12; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:600; text-transform:uppercase; }

    .report-header { background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%); border-bottom:1px solid #312e81; border-radius:16px; padding:32px 28px; margin-bottom:24px; position:relative; overflow:hidden; }
    .report-header::before { content:''; position:absolute; top:0;left:0;right:0;bottom:0; background:radial-gradient(circle at 70% 20%,#4f46e520 0%,transparent 50%); }
    .header-tag { font-size:11px; color:#818cf8; text-transform:uppercase; letter-spacing:2px; font-weight:700; margin-bottom:6px; position:relative; }
    .header-title { font-size:28px; font-weight:800; letter-spacing:-0.5px; color:#e2e8f0; position:relative; }
    .header-right { text-align:right; position:relative; }
    .header-period { font-size:14px; font-weight:700; color:#c7d2fe; }
    .header-gestor { font-size:11px; color:#64748b; margin-top:4px; }

    .creative-rank { display:flex; align-items:center; gap:16px; padding:16px 20px; border-radius:12px; margin-bottom:10px; flex-wrap:wrap; }
    .creative-rank-1 { background:linear-gradient(135deg,#1e1b4b40,#0f172a); border:1px solid #4f46e540; }
    .creative-rank-other { background:#ffffff04; border:1px solid #ffffff08; }
    .rank-badge { width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:900; color:#0a0e1a; flex-shrink:0; }

    .highlight-box { background:#fbbf2410; border:1px solid #fbbf2430; border-radius:8px; padding:14px 18px; margin-top:12px; }
    .highlight-box strong { color:#fbbf24; }

    .meta-card { background:#ffffff06; border:1px solid #ffffff08; border-radius:10px; padding:16px; text-align:center; }
    .meta-card-label { font-size:10px; color:#64748b; text-transform:uppercase; letter-spacing:1px; font-weight:600; }
    .meta-card-atual { font-size:12px; color:#94a3b8; margin-top:4px; }
    .meta-card-target { font-size:16px; color:#fbbf24; font-weight:800; margin-top:4px; }

    .report-footer { text-align:center; padding:24px 0 8px; border-top:1px solid #1e293b; margin-top:24px; }
    .footer-main { font-size:11px; color:#475569; }
    .footer-sub { font-size:10px; color:#334155; margin-top:4px; font-style:italic; }

    .upload-zone { background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%); border:2px dashed #818cf860; border-radius:20px; padding:60px 40px; text-align:center; margin:40px auto; max-width:700px; }
    .upload-icon { font-size:64px; margin-bottom:16px; }
    .upload-title { font-size:22px; font-weight:800; color:#e2e8f0; margin-bottom:8px; }
    .upload-sub { font-size:14px; color:#64748b; line-height:1.6; }

    [data-testid="stFileUploader"] { max-width: 500px; margin: 0 auto; }
    [data-testid="stFileUploader"] section { border: 1px solid #1e293b !important; border-radius: 12px !important; background: #0f172a !important; }
    [data-testid="stFileUploader"] button { background: #818cf8 !important; color: white !important; border-radius: 8px !important; }

    .demo-banner { background:linear-gradient(135deg,#fbbf2415,#f59e0b10); border:1px solid #fbbf2430; border-radius:10px; padding:10px 18px; margin-bottom:16px; text-align:center; font-size:12px; color:#fbbf24; font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNÇÕES AUXILIARES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def fmt_num(v):
    try:
        return f"{int(v):,.0f}".replace(",", ".")
    except:
        return "0"

def fmt_pct(v):
    try:
        return f"{float(v):.2f}%".replace(".", ",")
    except:
        return "0,00%"

def status_badge(s):
    s_str = str(s).strip()
    cls = f"badge-{s_str.lower()}"
    return f'<span class="{cls}">{s_str}</span>'

def plotly_dark(fig, height=320):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11), margin=dict(l=20, r=20, t=30, b=20), height=height,
        xaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
        legend=dict(font=dict(color="#94a3b8", size=10)),
        hoverlabel=dict(bgcolor="#1e293b", font_color="#e2e8f0", bordercolor="#333"),
    )
    return fig

def safe_div(a, b):
    try:
        return float(a) / float(b) if float(b) != 0 else 0
    except:
        return 0

def safe_float(v, default=0):
    try:
        return float(v)
    except:
        return default

def safe_int(v, default=0):
    try:
        return int(float(v))
    except:
        return default


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DADOS SINTÉTICOS PARA DEMONSTRAÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_demo_data():
    campanhas = pd.DataFrame([
        {"Campanha": "[CONV] Meta - Lookalike Compradores 1%", "Plataforma": "Meta Ads", "Tipo": "Conversão", "Objetivo": "Leads", "Status": "Ativa", "Investimento": 5800, "Impressões": 245000, "Alcance": 118000, "Cliques": 7120, "Leads": 412, "Vendas": 53, "Valor/Venda": 385},
        {"Campanha": "[CONV] Meta - Interesses Fitness", "Plataforma": "Meta Ads", "Tipo": "Conversão", "Objetivo": "Leads", "Status": "Ativa", "Investimento": 3400, "Impressões": 162000, "Alcance": 87000, "Cliques": 4380, "Leads": 248, "Vendas": 29, "Valor/Venda": 385},
        {"Campanha": "[RMK] Meta - Visitou LP 14d", "Plataforma": "Meta Ads", "Tipo": "Remarketing", "Objetivo": "Leads", "Status": "Ativa", "Investimento": 1900, "Impressões": 48000, "Alcance": 21000, "Cliques": 2640, "Leads": 186, "Vendas": 31, "Valor/Venda": 420},
        {"Campanha": "[RMK] Meta - Engajou IG 7d", "Plataforma": "Meta Ads", "Tipo": "Remarketing", "Objetivo": "Leads", "Status": "Ativa", "Investimento": 1200, "Impressões": 35000, "Alcance": 16500, "Cliques": 1890, "Leads": 124, "Vendas": 18, "Valor/Venda": 420},
        {"Campanha": "[TRAF] Meta - Vídeo View Educativo", "Plataforma": "Meta Ads", "Tipo": "Tráfego", "Objetivo": "Views", "Status": "Ativa", "Investimento": 800, "Impressões": 92000, "Alcance": 54000, "Cliques": 1420, "Leads": 38, "Vendas": 3, "Valor/Venda": 350},
        {"Campanha": "[SEARCH] Google - Marca", "Plataforma": "Google Ads", "Tipo": "Search", "Objetivo": "Conversões", "Status": "Ativa", "Investimento": 1100, "Impressões": 28000, "Alcance": 0, "Cliques": 3200, "Leads": 168, "Vendas": 42, "Valor/Venda": 395},
        {"Campanha": "[SEARCH] Google - Genérica Produto", "Plataforma": "Google Ads", "Tipo": "Search", "Objetivo": "Conversões", "Status": "Ativa", "Investimento": 2800, "Impressões": 72000, "Alcance": 0, "Cliques": 3850, "Leads": 192, "Vendas": 26, "Valor/Venda": 370},
        {"Campanha": "[SEARCH] Google - Concorrentes", "Plataforma": "Google Ads", "Tipo": "Search", "Objetivo": "Conversões", "Status": "Teste", "Investimento": 950, "Impressões": 31000, "Alcance": 0, "Cliques": 1180, "Leads": 54, "Vendas": 7, "Valor/Venda": 360},
        {"Campanha": "[DISPLAY] Google - Remarketing", "Plataforma": "Google Ads", "Tipo": "Display", "Objetivo": "Conversões", "Status": "Ativa", "Investimento": 750, "Impressões": 185000, "Alcance": 0, "Cliques": 920, "Leads": 41, "Vendas": 5, "Valor/Venda": 380},
        {"Campanha": "[PMAX] Google - Performance Max", "Plataforma": "Google Ads", "Tipo": "PMax", "Objetivo": "Conversões", "Status": "Teste", "Investimento": 1400, "Impressões": 110000, "Alcance": 0, "Cliques": 2100, "Leads": 87, "Vendas": 11, "Valor/Venda": 390},
        {"Campanha": "[CONV] TikTok - UGC Jovem", "Plataforma": "TikTok Ads", "Tipo": "Conversão", "Objetivo": "Leads", "Status": "Ativa", "Investimento": 1600, "Impressões": 320000, "Alcance": 195000, "Cliques": 4800, "Leads": 156, "Vendas": 12, "Valor/Venda": 310},
        {"Campanha": "[MSG] WhatsApp - Base Reativação", "Plataforma": "Meta Ads", "Tipo": "Mensagens", "Objetivo": "Vendas", "Status": "Pausada", "Investimento": 450, "Impressões": 12000, "Alcance": 5800, "Cliques": 480, "Leads": 62, "Vendas": 14, "Valor/Venda": 280},
    ])
    campanhas["Faturamento"] = campanhas["Vendas"] * campanhas["Valor/Venda"]
    campanhas["CTR"] = campanhas.apply(lambda r: safe_div(r["Cliques"], r["Impressões"]) * 100, axis=1)
    campanhas["CPC"] = campanhas.apply(lambda r: safe_div(r["Investimento"], r["Cliques"]), axis=1)
    campanhas["CPM"] = campanhas.apply(lambda r: safe_div(r["Investimento"], r["Impressões"]) * 1000, axis=1)
    campanhas["CPL"] = campanhas.apply(lambda r: safe_div(r["Investimento"], r["Leads"]), axis=1)
    campanhas["ROAS"] = campanhas.apply(lambda r: safe_div(r["Faturamento"], r["Investimento"]), axis=1)

    historico = pd.DataFrame([
        {"Mês": "Out/2025", "Investimento": 14200, "Impressões": 820000, "Cliques": 22400, "Leads": 1120, "Vendas": 145, "Faturamento": 54750},
        {"Mês": "Nov/2025", "Investimento": 16800, "Impressões": 940000, "Cliques": 26100, "Leads": 1340, "Vendas": 172, "Faturamento": 66040},
        {"Mês": "Dez/2025", "Investimento": 19500, "Impressões": 1080000, "Cliques": 28900, "Leads": 1480, "Vendas": 198, "Faturamento": 77220},
        {"Mês": "Jan/2026", "Investimento": 17200, "Impressões": 960000, "Cliques": 25600, "Leads": 1290, "Vendas": 168, "Faturamento": 65520},
        {"Mês": "Fev/2026", "Investimento": 18900, "Impressões": 1020000, "Cliques": 28200, "Leads": 1420, "Vendas": 189, "Faturamento": 73710},
        {"Mês": "Mar/2026", "Investimento": 22150, "Impressões": 1340000, "Cliques": 33980, "Leads": 1768, "Vendas": 251, "Faturamento": 96395},
    ])
    historico["CPL"] = historico.apply(lambda r: safe_div(r["Investimento"], r["Leads"]), axis=1)
    historico["CPA"] = historico.apply(lambda r: safe_div(r["Investimento"], r["Vendas"]), axis=1)
    historico["ROAS"] = historico.apply(lambda r: safe_div(r["Faturamento"], r["Investimento"]), axis=1)

    config = {
        "cliente": "FitPro Academy (DEMO)",
        "gestor": "Gestor Demonstração",
        "periodo": "01/03/2026 a 31/03/2026",
        "observacoes": [
            "Lookalike de compradores continua sendo o público com melhor CPL — R$ 14,08. Recomendo escalar em 20%.",
            "Remarketing de visitantes da LP teve ROAS de 6,83 — melhor retorno do mês. Criativos de depoimento puxaram o resultado.",
            "Campanha WhatsApp pausada por esgotamento da base. Reativar após nova captação de leads pelo funil orgânico.",
            "Google Search Marca mantém CPA baixíssimo (R$ 26,19). É a campanha mais eficiente em custo por venda.",
            "TikTok Ads com CPL de R$ 10,26 porém taxa de conversão baixa (7,7%). Leads precisam de mais aquecimento antes da oferta.",
            "PMAX ainda em aprendizado — manter por mais 2 semanas antes de avaliar corte.",
        ],
        "proximos_passos": [
            "Escalar Lookalike Compradores 1% em 20% de orçamento — manter CPL abaixo de R$ 16.",
            "Produzir 3 novos criativos em formato UGC para Meta e TikTok baseados nos depoimentos top.",
            "Criar sequência de e-mails de nutrição para leads do TikTok antes de direcionar para venda.",
            "Testar público lookalike 2% no Meta para ampliar alcance sem perder qualidade.",
            "Implementar Enhanced Conversions no Google Ads para melhorar otimização de campanhas Search.",
            "Agendar reunião de resultados com cliente na primeira semana de abril.",
        ],
    }
    return campanhas, historico, config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CARREGAMENTO DO EXCEL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_data(file):
    xls = pd.ExcelFile(file)
    df = pd.read_excel(xls, sheet_name="Campanhas")
    df = df[df["Campanha"].astype(str).str.upper() != "TOTAL"].copy()
    df = df.dropna(subset=["Campanha"]).reset_index(drop=True)

    num_cols = ["Investimento", "Impressões", "Alcance", "Cliques", "Leads", "Vendas", "Valor/Venda",
                "CTR", "CPC", "CPM", "CPL", "Faturamento", "ROAS", "Frequência"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    if "Faturamento" not in df.columns or df["Faturamento"].sum() == 0:
        df["Faturamento"] = df["Vendas"] * df["Valor/Venda"]
    if "CTR" not in df.columns or df["CTR"].sum() == 0:
        df["CTR"] = df.apply(lambda r: safe_div(r["Cliques"], r["Impressões"]) * 100, axis=1)
    if "CPC" not in df.columns or df["CPC"].sum() == 0:
        df["CPC"] = df.apply(lambda r: safe_div(r["Investimento"], r["Cliques"]), axis=1)
    if "CPM" not in df.columns or df["CPM"].sum() == 0:
        df["CPM"] = df.apply(lambda r: safe_div(r["Investimento"], r["Impressões"]) * 1000, axis=1)
    if "CPL" not in df.columns or df["CPL"].sum() == 0:
        df["CPL"] = df.apply(lambda r: safe_div(r["Investimento"], r["Leads"]), axis=1)
    if "ROAS" not in df.columns or df["ROAS"].sum() == 0:
        df["ROAS"] = df.apply(lambda r: safe_div(r["Faturamento"], r["Investimento"]), axis=1)

    hist = None
    if "Histórico Mensal" in xls.sheet_names:
        hist = pd.read_excel(xls, sheet_name="Histórico Mensal")
        for c in ["Investimento", "Impressões", "Cliques", "Leads", "Vendas", "Faturamento", "CPL", "CPA", "ROAS"]:
            if c in hist.columns:
                hist[c] = pd.to_numeric(hist[c], errors="coerce").fillna(0)

    config = {"cliente": "Cliente", "gestor": "Gestor", "periodo": "Período"}
    if "Configurações" in xls.sheet_names:
        cfg = pd.read_excel(xls, sheet_name="Configurações", header=None)
        cfg_dict = dict(zip(cfg[0].astype(str), cfg[1].astype(str)))
        config["cliente"] = cfg_dict.get("Nome do Cliente", "Cliente")
        config["gestor"] = cfg_dict.get("Gestor Responsável", "Gestor")
        config["periodo"] = cfg_dict.get("Período do Relatório", "Período")

        obs, passos = [], []
        in_obs, in_passos = False, False
        for _, row in cfg.iterrows():
            key = str(row[0]).strip() if pd.notna(row[0]) else ""
            val = str(row[1]).strip() if pd.notna(row[1]) else ""
            if "OBSERV" in key.upper():
                in_obs, in_passos = True, False
                continue
            if "PRÓXIMOS" in key.upper() or "PROXIMOS" in key.upper():
                in_obs, in_passos = False, True
                continue
            if key == "" and val == "":
                in_obs, in_passos = False, False
                continue
            if in_obs and val:
                obs.append(val)
            if in_passos and val:
                passos.append(val)
        config["observacoes"] = obs
        config["proximos_passos"] = passos

    return df, hist, config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# APP PRINCIPAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if "df" not in st.session_state:
    st.markdown("")
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📊</div>
        <div class="upload-title">Relatório de Tráfego Pago</div>
        <div class="upload-sub">
            Estilo Comunidade Sobral de Tráfego<br>
            <span style="color:#818cf8;font-weight:600;">Faça upload do seu arquivo Excel (.xlsx)</span> com os dados das campanhas
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_up = st.columns([1, 2, 1])[1]
    with col_up:
        uploaded = st.file_uploader("", type=["xlsx", "xls"], label_visibility="collapsed")
        if uploaded:
            try:
                df, hist, config = load_data(uploaded)
                st.session_state["df"] = df
                st.session_state["hist"] = hist
                st.session_state["config"] = config
                st.session_state["is_demo"] = False
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}")

        st.markdown("")
        if st.button("🧪 Demonstração com dados sintéticos", use_container_width=True, type="secondary"):
            df_demo, hist_demo, config_demo = generate_demo_data()
            st.session_state["df"] = df_demo
            st.session_state["hist"] = hist_demo
            st.session_state["config"] = config_demo
            st.session_state["is_demo"] = True
            st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:24px;padding:20px;">
        <div style="font-size:13px;color:#64748b;font-weight:600;margin-bottom:12px;">📋 O arquivo deve conter a aba "Campanhas" com as colunas:</div>
        <div style="display:inline-block;text-align:left;background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:16px 24px;">
            <code style="color:#818cf8;font-size:12px;line-height:2;">
            Campanha | Plataforma | Tipo | Objetivo | Status | Investimento | Impressões | Alcance | Cliques | Leads | Vendas | Valor/Venda
            </code>
        </div>
        <div style="font-size:11px;color:#475569;margin-top:12px;">
            Abas opcionais: <strong style="color:#94a3b8;">Histórico Mensal</strong> e <strong style="color:#94a3b8;">Configurações</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ── DADOS CARREGADOS ──
df = st.session_state["df"]
hist = st.session_state.get("hist")
config = st.session_state["config"]
is_demo = st.session_state.get("is_demo", False)

inv_total = df["Investimento"].sum()
leads_total = safe_int(df["Leads"].sum())
vendas_total = safe_int(df["Vendas"].sum())
fat_total = df["Faturamento"].sum()
cliques_total = safe_int(df["Cliques"].sum())
impressoes_total = safe_int(df["Impressões"].sum())
alcance_total = safe_int(df["Alcance"].sum()) if "Alcance" in df.columns else 0

roas_total = safe_div(fat_total, inv_total)
cpl_total = safe_div(inv_total, leads_total)
cpa_total = safe_div(inv_total, vendas_total)
taxa_conv = safe_div(vendas_total, leads_total) * 100
ticket_medio = safe_div(fat_total, vendas_total)
lucro_bruto = fat_total - inv_total

has_plataforma = "Plataforma" in df.columns
if has_plataforma:
    plataformas = df.groupby("Plataforma").agg(
        {"Investimento": "sum", "Leads": "sum", "Vendas": "sum", "Faturamento": "sum", "Cliques": "sum", "Impressões": "sum"}
    ).reset_index()

if is_demo:
    st.markdown('<div class="demo-banner">⚠️ MODO DEMONSTRAÇÃO — Dados sintéticos para visualização do layout. Faça upload do seu Excel para ver seus dados reais.</div>', unsafe_allow_html=True)

col_btn = st.columns([6, 1])
with col_btn[1]:
    if st.button("🔄 Trocar arquivo", use_container_width=True):
        for k in ["df", "hist", "config", "is_demo"]:
            st.session_state.pop(k, None)
        st.rerun()

# ── HEADER ──
st.markdown(f"""
<div class="report-header">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
        <div>
            <div class="header-tag">📊 Relatório de Tráfego Pago</div>
            <div class="header-title">{config['cliente']}</div>
        </div>
        <div class="header-right">
            <div style="font-size:12px;color:#94a3b8;">Período</div>
            <div class="header-period">{config['periodo']}</div>
            <div class="header-gestor">Gestor: {config['gestor']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_visao, tab_campanhas, tab_plataformas, tab_criativos, tab_plano = st.tabs([
    "📈 Visão Geral", "📋 Campanhas", "📱 Plataformas", "🏆 Top Campanhas", "🎯 Plano de Ação",
])


# ═══════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ═══════════════════════════════════════════════════════════
with tab_visao:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Investimento Total", fmt_brl(inv_total))
    c2.metric("🎯 Leads Gerados", fmt_num(leads_total), f"CPL: {fmt_brl(cpl_total)}")
    c3.metric("🛒 Vendas", fmt_num(vendas_total), f"Conv: {fmt_pct(taxa_conv)}")
    c4.metric("📈 Faturamento", fmt_brl(fat_total), f"ROAS: {roas_total:.2f}x")

    st.markdown("")

    st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Métricas Secundárias</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
    for col, label, val in [
        (sc1, "CPA", fmt_brl(cpa_total)),
        (sc2, "CPL Médio", fmt_brl(cpl_total)),
        (sc3, "ROAS", f"{roas_total:.2f}x"),
        (sc4, "Conv. Lead→Venda", fmt_pct(taxa_conv)),
        (sc5, "Ticket Médio", fmt_brl(ticket_medio)),
        (sc6, "Lucro Bruto", fmt_brl(lucro_bruto)),
    ]:
        col.markdown(f'<div class="kpi-box"><div class="kpi-label">{label}</div><div class="kpi-value">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("")

    if hist is not None and not hist.empty:
        st.markdown('<div class="section-header"><span class="section-bar" style="background:#34d399;"></span> Evolução Mensal</div>', unsafe_allow_html=True)
        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            fig = go.Figure(go.Bar(x=hist["Mês"].tolist(), y=hist["Leads"].tolist(), marker=dict(color="#34d399", cornerradius=6), text=hist["Leads"].astype(int).tolist(), textposition="outside", textfont=dict(color="#94a3b8", size=10)))
            fig.update_layout(title=dict(text="Leads", font=dict(size=13, color="#64748b")))
            plotly_dark(fig); st.plotly_chart(fig, use_container_width=True)
        with gc2:
            fig = go.Figure(go.Bar(x=hist["Mês"].tolist(), y=hist["Vendas"].tolist(), marker=dict(color="#818cf8", cornerradius=6), text=hist["Vendas"].astype(int).tolist(), textposition="outside", textfont=dict(color="#94a3b8", size=10)))
            fig.update_layout(title=dict(text="Vendas", font=dict(size=13, color="#64748b")))
            plotly_dark(fig); st.plotly_chart(fig, use_container_width=True)
        with gc3:
            fig = go.Figure(go.Bar(x=hist["Mês"].tolist(), y=hist["Investimento"].tolist(), marker=dict(color="#f59e0b", cornerradius=6), text=[f"R${v/1000:.1f}k" for v in hist["Investimento"]], textposition="outside", textfont=dict(color="#94a3b8", size=10)))
            fig.update_layout(title=dict(text="Investimento", font=dict(size=13, color="#64748b")))
            plotly_dark(fig); st.plotly_chart(fig, use_container_width=True)

    if has_plataforma and len(plataformas) > 1:
        st.markdown('<div class="section-header"><span class="section-bar" style="background:#f59e0b;"></span> Distribuição de Investimento</div>', unsafe_allow_html=True)
        di1, di2 = st.columns(2)
        colors_list = ["#818cf8", "#34d399", "#f59e0b", "#f87171", "#a78bfa", "#fb923c"]
        with di1:
            fig = go.Figure(go.Pie(labels=plataformas["Plataforma"].tolist(), values=plataformas["Investimento"].tolist(), marker=dict(colors=colors_list[:len(plataformas)]), hole=0.55, textinfo="label+percent", textfont=dict(color="#e2e8f0", size=11)))
            fig.update_layout(showlegend=False); plotly_dark(fig, 300); st.plotly_chart(fig, use_container_width=True)
        with di2:
            bars_html = ""
            for i, (_, row) in enumerate(plataformas.iterrows()):
                pct = safe_div(row["Investimento"], inv_total) * 100
                color = colors_list[i % len(colors_list)]
                bars_html += f"""
                <div style="margin-bottom:16px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                        <span style="color:{color};font-weight:700;">{row['Plataforma']}</span>
                        <span style="color:#94a3b8;">{fmt_brl(row['Investimento'])} ({pct:.0f}%)</span>
                    </div>
                    <div style="width:100%;height:8px;background:#ffffff10;border-radius:4px;">
                        <div style="width:{pct}%;height:100%;background:{color};border-radius:4px;"></div>
                    </div>
                </div>"""
            st.markdown(f'<div style="padding:20px;">{bars_html}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 2 — CAMPANHAS
# ═══════════════════════════════════════════════════════════
with tab_campanhas:
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Todas as Campanhas</div>', unsafe_allow_html=True)

    th_style = "padding:12px;text-align:right;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;"
    rows = ""
    for _, r in df.iterrows():
        cpl_val = safe_float(r.get("CPL", 0))
        cpl_color = "#34d399" if cpl_val < 15 else ("#fbbf24" if cpl_val < 30 else "#f87171")
        plat = r.get("Plataforma", "-") if has_plataforma else "-"
        status = r.get("Status", "-") if "Status" in df.columns else "-"
        rows += f"""<tr style="border-bottom:1px solid #ffffff08;">
            <td style="padding:12px;font-size:12px;font-weight:600;color:#cbd5e1;max-width:260px;">{r['Campanha']}</td>
            <td style="padding:12px;font-size:12px;color:#94a3b8;">{plat}</td>
            <td style="padding:12px;text-align:right;font-family:monospace;color:#cbd5e1;">{fmt_brl(r['Investimento'])}</td>
            <td style="padding:12px;text-align:right;color:#cbd5e1;">{fmt_num(r['Impressões'])}</td>
            <td style="padding:12px;text-align:right;color:#cbd5e1;">{fmt_num(r['Cliques'])}</td>
            <td style="padding:12px;text-align:right;font-weight:700;color:#34d399;">{safe_int(r['Leads'])}</td>
            <td style="padding:12px;text-align:right;color:{cpl_color};font-weight:700;">{fmt_brl(r['CPL'])}</td>
            <td style="padding:12px;text-align:right;font-weight:700;color:#818cf8;">{safe_int(r['Vendas'])}</td>
            <td style="padding:12px;text-align:right;color:#cbd5e1;">{fmt_brl(r['Faturamento'])}</td>
            <td style="padding:12px;text-align:right;color:#cbd5e1;">{safe_float(r['ROAS']):.2f}x</td>
            <td style="padding:12px;text-align:center;">{status_badge(status)}</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:14px;overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;min-width:900px;">
            <thead><tr style="border-bottom:1px solid #1e293b;">
                <th style="padding:12px;text-align:left;{th_style[8:]}">Campanha</th>
                <th style="padding:12px;text-align:left;{th_style[8:]}">Plataforma</th>
                <th style="{th_style}">Investido</th>
                <th style="{th_style}">Impressões</th>
                <th style="{th_style}">Cliques</th>
                <th style="{th_style}">Leads</th>
                <th style="{th_style}">CPL</th>
                <th style="{th_style}">Vendas</th>
                <th style="{th_style}">Faturamento</th>
                <th style="{th_style}">ROAS</th>
                <th style="padding:12px;text-align:center;font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;">Status</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown('<div class="section-header"><span class="section-bar" style="background:#a78bfa;"></span> CPL por Campanha</div>', unsafe_allow_html=True)
    sorted_df = df.sort_values("CPL", ascending=True)
    fig = go.Figure(go.Bar(
        y=sorted_df["Campanha"].str[:35].tolist(), x=sorted_df["CPL"].tolist(), orientation="h",
        marker=dict(color=["#34d399" if v < 15 else ("#fbbf24" if v < 30 else "#f87171") for v in sorted_df["CPL"]], cornerradius=4),
        text=[fmt_brl(v) for v in sorted_df["CPL"]], textposition="outside", textfont=dict(color="#94a3b8", size=10),
    ))
    plotly_dark(fig, max(250, len(df) * 35)); fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — PLATAFORMAS
# ═══════════════════════════════════════════════════════════
with tab_plataformas:
    if has_plataforma:
        for _, plat_row in plataformas.iterrows():
            plat_name = plat_row["Plataforma"]
            plat_df = df[df["Plataforma"] == plat_name]
            plat_inv = plat_row["Investimento"]
            plat_leads = safe_int(plat_row["Leads"])
            plat_vendas = safe_int(plat_row["Vendas"])
            plat_fat = plat_row["Faturamento"]

            st.markdown(f'<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> {plat_name}</div>', unsafe_allow_html=True)

            p1, p2, p3, p4, p5 = st.columns(5)
            p1.metric("Investido", fmt_brl(plat_inv))
            p2.metric("Leads", fmt_num(plat_leads), f"CPL: {fmt_brl(safe_div(plat_inv, plat_leads))}")
            p3.metric("Vendas", fmt_num(plat_vendas))
            p4.metric("Faturamento", fmt_brl(plat_fat))
            p5.metric("ROAS", f"{safe_div(plat_fat, plat_inv):.2f}x")

            p_rows = ""
            for _, r in plat_df.iterrows():
                status = r.get("Status", "-") if "Status" in df.columns else "-"
                p_rows += f"""<tr style="border-bottom:1px solid #ffffff08;">
                    <td style="padding:10px;font-size:12px;font-weight:600;color:#cbd5e1;">{r['Campanha']}</td>
                    <td style="padding:10px;text-align:right;font-family:monospace;color:#cbd5e1;">{fmt_brl(r['Investimento'])}</td>
                    <td style="padding:10px;text-align:right;color:#34d399;font-weight:700;">{safe_int(r['Leads'])}</td>
                    <td style="padding:10px;text-align:right;color:#cbd5e1;">{fmt_brl(r['CPL'])}</td>
                    <td style="padding:10px;text-align:right;color:#818cf8;font-weight:700;">{safe_int(r['Vendas'])}</td>
                    <td style="padding:10px;text-align:right;color:#cbd5e1;">{safe_float(r['ROAS']):.2f}x</td>
                    <td style="padding:10px;text-align:center;">{status_badge(status)}</td>
                </tr>"""
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;overflow:hidden;margin-bottom:24px;">
                <table style="width:100%;border-collapse:collapse;">
                    <thead><tr style="border-bottom:1px solid #1e293b;">
                        <th style="padding:10px;text-align:left;font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;">Campanha</th>
                        <th style="padding:10px;text-align:right;font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;">Investido</th>
                        <th style="padding:10px;text-align:right;font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;">Leads</th>
                        <th style="padding:10px;text-align:right;font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;">CPL</th>
                        <th style="padding:10px;text-align:right;font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;">Vendas</th>
                        <th style="padding:10px;text-align:right;font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;">ROAS</th>
                        <th style="padding:10px;text-align:center;font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;">Status</th>
                    </tr></thead>
                    <tbody>{p_rows}</tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("A coluna **Plataforma** não foi encontrada no arquivo. Adicione-a para ver a análise por plataforma.")


# ═══════════════════════════════════════════════════════════
# TAB 4 — TOP CAMPANHAS
# ═══════════════════════════════════════════════════════════
with tab_criativos:
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#f59e0b;"></span> Top Campanhas por CPL (Menor = Melhor)</div>', unsafe_allow_html=True)

    top_cpl = df[df["Leads"] > 0].nsmallest(5, "CPL")
    for i, (_, r) in enumerate(top_cpl.iterrows()):
        rank_bg = "#fbbf24" if i == 0 else ("#94a3b8" if i == 1 else "#b45309" if i == 2 else "#475569")
        rank_class = "creative-rank-1" if i == 0 else "creative-rank-other"
        tipo = r.get("Tipo", "") if "Tipo" in df.columns else ""
        st.markdown(f"""
        <div class="creative-rank {rank_class}">
            <div class="rank-badge" style="background:{rank_bg};">{i+1}</div>
            <div style="flex:1 1 200px;min-width:150px;">
                <div style="font-size:15px;font-weight:700;color:#e2e8f0;">{r['Campanha']}</div>
                <div style="font-size:11px;color:#64748b;margin-top:2px;">{tipo}</div>
            </div>
            <div style="display:flex;gap:28px;flex-wrap:wrap;">
                <div style="text-align:center;"><div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:600;">CPL</div><div style="font-size:18px;font-weight:800;color:#34d399;margin-top:2px;">{fmt_brl(r['CPL'])}</div></div>
                <div style="text-align:center;"><div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:600;">Leads</div><div style="font-size:18px;font-weight:800;color:#818cf8;margin-top:2px;">{safe_int(r['Leads'])}</div></div>
                <div style="text-align:center;"><div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:600;">ROAS</div><div style="font-size:18px;font-weight:800;color:#fbbf24;margin-top:2px;">{safe_float(r['ROAS']):.2f}x</div></div>
                <div style="text-align:center;"><div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:600;">Vendas</div><div style="font-size:18px;font-weight:800;color:#f59e0b;margin-top:2px;">{safe_int(r['Vendas'])}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Top Campanhas por ROAS (Maior = Melhor)</div>', unsafe_allow_html=True)

    top_roas = df[df["Vendas"] > 0].nlargest(5, "ROAS")
    for i, (_, r) in enumerate(top_roas.iterrows()):
        rank_bg = "#fbbf24" if i == 0 else ("#94a3b8" if i == 1 else "#b45309" if i == 2 else "#475569")
        rank_class = "creative-rank-1" if i == 0 else "creative-rank-other"
        st.markdown(f"""
        <div class="creative-rank {rank_class}">
            <div class="rank-badge" style="background:{rank_bg};">{i+1}</div>
            <div style="flex:1 1 200px;min-width:150px;">
                <div style="font-size:15px;font-weight:700;color:#e2e8f0;">{r['Campanha']}</div>
            </div>
            <div style="display:flex;gap:28px;flex-wrap:wrap;">
                <div style="text-align:center;"><div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:600;">ROAS</div><div style="font-size:18px;font-weight:800;color:#fbbf24;margin-top:2px;">{safe_float(r['ROAS']):.2f}x</div></div>
                <div style="text-align:center;"><div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:600;">Faturamento</div><div style="font-size:18px;font-weight:800;color:#34d399;margin-top:2px;">{fmt_brl(r['Faturamento'])}</div></div>
                <div style="text-align:center;"><div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:600;">Investido</div><div style="font-size:18px;font-weight:800;color:#818cf8;margin-top:2px;">{fmt_brl(r['Investimento'])}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── GRÁFICO SCATTER CORRIGIDO ──
    # Erro original: colorbar=dict(title="ROAS", titlefont=dict(...))
    # titlefont foi removido em versões recentes do Plotly.
    # Correção: usar title=dict(text=..., font=dict(...))
    # Também convertemos todas as Series para .tolist() para evitar
    # problemas de serialização com pandas em Python 3.14+
    st.markdown('<div class="section-header"><span class="section-bar" style="background:#34d399;"></span> Investimento vs ROAS</div>', unsafe_allow_html=True)

    scatter_sizes = [max(s, 3) * 1.5 for s in df["Vendas"].tolist()]
    scatter_colors = df["ROAS"].tolist()

    fig = go.Figure(go.Scatter(
        x=df["Investimento"].tolist(),
        y=df["ROAS"].tolist(),
        mode="markers+text",
        text=df["Campanha"].str[:20].tolist(),
        textposition="top center",
        textfont=dict(color="#94a3b8", size=9),
        marker=dict(
            size=scatter_sizes,
            color=scatter_colors,
            colorscale=[[0, "#f87171"], [0.5, "#fbbf24"], [1, "#34d399"]],
            showscale=True,
            colorbar=dict(
                title=dict(text="ROAS", font=dict(color="#94a3b8")),
                tickfont=dict(color="#94a3b8"),
            ),
        ),
    ))
    plotly_dark(fig, 400)
    fig.update_layout(
        xaxis_title="Investimento (R$)",
        yaxis_title="ROAS",
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 5 — PLANO DE AÇÃO
# ═══════════════════════════════════════════════════════════
with tab_plano:
    obs_list = config.get("observacoes", [])
    passos_list = config.get("proximos_passos", [])

    if obs_list:
        st.markdown('<div class="section-header"><span class="section-bar" style="background:#818cf8;"></span> Observações do Gestor</div>', unsafe_allow_html=True)
        obs_html = ""
        for i, obs in enumerate(obs_list, 1):
            obs_html += f'<div class="obs-card"><span class="obs-num">{str(i).zfill(2)}</span><span class="obs-text">{obs}</span></div>'
        st.markdown(obs_html, unsafe_allow_html=True)
        st.markdown("")

    if passos_list:
        st.markdown('<div class="section-header"><span class="section-bar" style="background:#34d399;"></span> Próximos Passos</div>', unsafe_allow_html=True)
        act_html = ""
        for i, p in enumerate(passos_list, 1):
            act_html += f'<div class="action-card"><div class="action-num">{i}</div><span class="action-text">{p}</span></div>'
        st.markdown(act_html, unsafe_allow_html=True)
        st.markdown("")

    if not obs_list and not passos_list:
        st.info("Adicione a aba **Configurações** ao seu Excel com as seções 'OBSERVAÇÕES DO GESTOR' e 'PRÓXIMOS PASSOS' para ver o plano de ação aqui.")

    if hist is not None and not hist.empty:
        st.markdown('<div class="section-header"><span class="section-bar" style="background:#a78bfa;"></span> Tendência de Crescimento</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["Mês"].tolist(), y=hist["Faturamento"].tolist(),
            mode="lines+markers+text", name="Faturamento",
            line=dict(color="#818cf8", width=3), marker=dict(size=8),
            text=[f"R${v/1000:.0f}k" for v in hist["Faturamento"]],
            textposition="top center", textfont=dict(color="#94a3b8", size=10),
        ))
        fig.add_trace(go.Scatter(
            x=hist["Mês"].tolist(), y=hist["Investimento"].tolist(),
            mode="lines+markers+text", name="Investimento",
            line=dict(color="#f59e0b", width=2, dash="dot"), marker=dict(size=6),
            text=[f"R${v/1000:.1f}k" for v in hist["Investimento"]],
            textposition="bottom center", textfont=dict(color="#94a3b8", size=9),
        ))
        plotly_dark(fig, 320)
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)


# ── FOOTER ──
st.markdown(f"""
<div class="report-footer">
    <div class="footer-main">Relatório gerado por {config['gestor']} • Estilo Comunidade Sobral de Tráfego</div>
    <div class="footer-sub">"Coleta → Análise → Ação" — O ciclo que gera resultado.</div>
</div>
""", unsafe_allow_html=True)
