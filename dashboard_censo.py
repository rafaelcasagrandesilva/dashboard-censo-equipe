import streamlit as st
import pandas as pd
import datetime
import base64
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard Censo - M&E Engenharia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Função para converter imagem local para base64
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 2. ESTILIZAÇÃO CSS CUSTOMIZADA (CABEÇALHO FIXO)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 6rem !important; 
        padding-bottom: 2rem !important;
        max-width: 1400px;
    }

    /* Header Fixo (Sticky) */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #E5E7EB;
        padding: 0.6rem 2rem;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .logo-img {
        height: 45px; /* Aumentado um pouco para destaque */
        width: auto;
    }

    .logo-text {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E3A8A;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .last-update {
        font-size: 0.8rem;
        color: #6B7280;
    }

    /* Títulos */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2.5rem;
    }

    /* Cards de KPI */
    .kpi-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #3B82F6;
    }

    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
    }

    /* Cards de Agentes */
    .agent-card {
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    
    .status-success { background: linear-gradient(135deg, #10B981 0%, #059669 100%); }
    .status-warning { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); }
    .status-danger { background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); }

    .agent-name { font-size: 1rem; font-weight: 600; margin-bottom: 0.25rem; }
    .agent-value { font-size: 1.5rem; font-weight: 700; }
    .agent-status { font-size: 0.7rem; text-transform: uppercase; font-weight: 600; opacity: 0.9; }

    /* Esconder elementos padrão do Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. CARREGAMENTO E TRATAMENTO DE DADOS
@st.cache_data(ttl=600)
def load_data():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSfLPS2shPGfYe72_qhFGeTeFuMcJuurpKh1mIe73knOlO-GbSlsCdFv64Og0utVkcZ3WW8IaHKfIG/pub?output=csv"
    df = pd.read_csv(SHEET_URL)
    cols_to_drop = ["Unnamed: 0", "Meta", "Meta.1", "Meta.2", "Meta.3", "Meta.4", "250", "Unnamed: 15", "Unnamed: 13", "1000"]
    df = df.drop(columns=cols_to_drop, errors="ignore")
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df["% Meta"] = df["% Meta"].astype(str).str.replace("%", "", regex=False).astype(float)
    dias_semana = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"}
    df["Dia"] = df["Data"].dt.weekday.map(dias_semana)
    df["Data_fmt"] = df["Data"].dt.strftime("%d/%m/%Y")
    return df

try:
    df = load_data()
    
    # Cálculos
    df_produtivo = df[df["Total"] > 0]
    producao_total = df["Total"].sum()
    faturamento_previsto = producao_total * 1.16
    producao_media_dia = df_produtivo["Total"].mean()
    melhor_dia_row = df.loc[df["Total"].idxmax()]
    media_meta = df_produtivo["% Meta"].mean()

    # Meta Individual Acumulada
    data_inicio = pd.to_datetime("2026-01-13")
    meta_diaria = 250
    data_hoje = pd.Timestamp.today().normalize()
    dias_uteis = pd.bdate_range(start=data_inicio, end=data_hoje).size
    meta_individual_acumulada = dias_uteis * meta_diaria

    # --- CABEÇALHO FIXO COM LOGO CORRIGIDO ---
    # Caminho exato conforme sua imagem do VS Code
    logo_path = os.path.join("assets", "logo_sem_borda.png")
    logo_base64 = get_base64_of_bin_file(logo_path)
    
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img">' if logo_base64 else ""
    
    st.markdown(f"""
    <div class="fixed-header">
        <div class="header-left">
            {logo_html}
            <p class="logo-text">M&E ENGENHARIA</p>
        </div>
        <div class="last-update">Atualizado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- CONTEÚDO PRINCIPAL ---
    st.markdown('<div class="main-title">Dashboard do Censo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Visão Geral da Performance e Acompanhamento da Equipe</div>', unsafe_allow_html=True)

    # KPIs PRINCIPAIS
    kpi_cols = st.columns(5)

    with kpi_cols[0]:
        st.markdown(
            f'''
            <div class="kpi-card">
                <div class="kpi-label">Faturamento Estimado</div>
                <div class="kpi-value">R$ {faturamento_previsto:,.2f}</div>
            </div>
            '''.replace(',', 'X').replace('.', ',').replace('X', '.'),
            unsafe_allow_html=True
        )

    with kpi_cols[1]:
        st.markdown(
            f'''
            <div class="kpi-card">
                <div class="kpi-label">Produção Total</div>
                <div class="kpi-value">{producao_total:,.0f}</div>
            </div>
            '''.replace(',', '.'),
            unsafe_allow_html=True
        )

    with kpi_cols[2]:
        st.markdown(
            f'''
            <div class="kpi-card">
                <div class="kpi-label">Média Diária</div>
                <div class="kpi-value">{producao_media_dia:,.0f}</div>
            </div>
            '''.replace(',', '.'),
            unsafe_allow_html=True
        )

    with kpi_cols[3]:
        st.markdown(
            f'''
            <div class="kpi-card">
                <div class="kpi-label">Recorde Diário</div>
                <div class="kpi-value">{melhor_dia_row["Total"]:,.0f}</div>
            </div>
            '''.replace(',', '.'),
            unsafe_allow_html=True
        )

    with kpi_cols[4]:
        st.markdown(
            f'''
            <div class="kpi-card">
                <div class="kpi-label">Atingimento Meta</div>
                <div class="kpi-value">{media_meta:.1f}%</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # STATUS DA EQUIPE
    st.subheader("🎯 Meta Individual e Status da Equipe")
    agentes = ["Gabriel", "Leandro", "Rony", "Willa"]
    cols_agentes = st.columns(len(agentes) + 1)
    
    with cols_agentes[0]:
        st.markdown(f'<div class="agent-card status-warning"><div class="agent-name">Meta Alvo</div><div class="agent-value">{meta_individual_acumulada:,.0f}</div><div class="agent-status">Acumulado</div></div>'.replace(',', '.'), unsafe_allow_html=True)

    celulas_resumo = {
        "Gabriel": (33, 15),  # P34
        "Leandro": (34, 15),  # P35
        "Rony": (35, 15),     # P36
        "Willa": (36, 15)     # P37
    }

    for i, agente in enumerate(agentes):

        if agente in celulas_resumo:
            linha, coluna = celulas_resumo[agente]
            total_agente = df.iloc[linha, coluna]
        else:
            total_agente = df[agente].sum()

        if total_agente >= meta_individual_acumulada:
            status_class, status_text = "status-success", "Meta Atingida"
        elif total_agente >= (meta_individual_acumulada * 0.8):
            status_class, status_text = "status-warning", "Em Atenção"
        else:
            status_class, status_text = "status-danger", "Abaixo da Meta"
            
        with cols_agentes[i+1]:
            st.markdown(
                f'<div class="agent-card {status_class}">'
                f'<div class="agent-name">{agente}</div>'
                f'<div class="agent-value">{total_agente:,.0f}</div>'
                f'<div class="agent-status">{status_text}</div>'
                f'</div>'.replace(',', '.'),
                unsafe_allow_html=True
            )

    # TABELA DETALHADA
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Histórico de Produção (Últimos 10 dias)"):
        # Últimos 10 dias (incluindo dias com produção zero), até a data atual
        data_hoje = pd.Timestamp.today().normalize()

        df_tabela = (
            df[df["Data"] <= data_hoje]
            .sort_values("Data", ascending=False)
            .head(10)
            .sort_values("Data")
            .copy()
        )

        df_tabela = df_tabela[["Dia", "Data_fmt", "Gabriel", "Leandro", "Rony", "Willa", "Total", "% Meta"]]

        st.dataframe(
            df_tabela.rename(columns={"Data_fmt": "Data"}),
            use_container_width=True,
            hide_index=True,
            column_config={
                "% Meta": st.column_config.NumberColumn(format="%.1f%%"),
                "Total": st.column_config.NumberColumn(format="%d")
            }
        )

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

# Rodapé
st.markdown('<div style="text-align: center; color: #9CA3AF; font-size: 0.8rem; margin-top: 3rem; padding-bottom: 1rem;">Desenvolvido para M&E Engenharia • 2026</div>', unsafe_allow_html=True)
