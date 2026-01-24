#RODE COMO: streamlit run dashboard_censo.py

import streamlit as st
import pandas as pd

#CONFIGURAR A PÁGINA DO DASHBOARD

st.set_page_config(
    page_title="Dashboard Censo - Visão Geral", #título da aba do navegador
    layout="wide" #largura da tela (tela cheia)
)

#TÍTULOS E SUBTÍTULOS VISÍVEIS

st.title("Dashboard do Censo - Visão Geral da Equipe")
st.caption("Acompanhamento de produção da equipe de análise")

#LER A PLANILHA COM PANDAS

SHEET_URL="https://docs.google.com/spreadsheets/d/e/2PACX-1vSSfLPS2shPGfYe72_qhFGeTeFuMcJuurpKh1mIe73knOlO-GbSlsCdFv64Og0utVkcZ3WW8IaHKfIG/pub?output=csv"

df = pd.read_csv(SHEET_URL)

#REMOVER COLUNAS QUE NÃO SERVEM

df = df.drop(
    columns=["Unnamed: 0", "Meta", "Meta.1", "Meta.2", "Meta.3", "Meta.4", "250", "Unnamed: 15", "Unnamed: 13","1000"],
    errors="ignore"
)

#CONVERTER A COLUNA DATA (linha por linha)

df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)

#TRATAR A COLUNA %META

df["% Meta"] = df["% Meta"].str.replace("%", "").astype(float)

#INÍCIO DOS KPIS

df_produtivo = df[df["Total"] > 0]
producao_total = df["Total"].sum()
producao_media_dia = df_produtivo["Total"].mean()
melhor_dia = df.loc[df["Total"].idxmax()]
media_meta = df_produtivo["% Meta"].mean()

#TRANSFORMAR KPIs EM CARD (st.metric)

st.markdown("""
<style>
.card {
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    font-weight: 400;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
}

.card-green {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: #e8f5e9;
}

.card-red {
    background: linear-gradient(135deg, #7f1d1d, #991b1b);
    color: #fee2e2;
}

.card-yellow {
    background: linear-gradient(135deg, #92400e, #b45309);
    color: #fff7ed;
}

.card-title {
    font-size: 22px;
    opacity: 0.9;
}

.card-value {
    font-size: 34px;
    margin-top: 6px;
}

.card-sub {
    font-size: 14px;
    margin-top: 6px;
    opacity: 0.85;
}


</style>
           
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)


#CARD 1 - Produção Total
with col1:
 st.markdown(f"""
    <div class="card card-hover">
        <div class="card-title">Produção Total</div>
        <div class="card-value">{producao_total:,}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

#CARD 2 - Produção Média por Dia
with col2:
 st.markdown(f"""
    <div class="card card-hover">
        <div class="card-title">Produção Média / Dia</div>
        <div class="card-value">{producao_media_dia:.0f}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

#CARD 3 - Melhor Dia
with col3:
    st.markdown(f"""
    <div class="card card-hover">
        <div class="card-title">Melhor Dia (Produção)</div>
        <div class="card-value">{melhor_dia['Total']}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

#CARD 4 - Média % Meta
with col4:
   st.markdown(f"""
    <div class="card card-hover">
        <div class="card-title">Média % da Meta</div>
        <div class="card-value">{media_meta:.1f}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

st.divider()

#CÁLCULO DA META INDIVIDUAL ACUMULADA (equivalente à célula P2 do Excel)

data_inicio = pd.to_datetime("2026-01-13")
meta_diaria = 250

data_hoje = pd.Timestamp.today().normalize()

dias_uteis = pd.bdate_range(
    start=data_inicio,
    end=data_hoje
).size

meta_individual = dias_uteis * meta_diaria

#total acumulado
total_gabriel = df["Gabriel"].sum()
total_leandro = df["Leandro"].sum()
total_rony = df["Rony"].sum()
total_willa = df["Willa"].sum()

#cores
status_gabriel = total_gabriel >= meta_individual
status_leandro = total_leandro >= meta_individual
status_rony = total_rony >= meta_individual
status_willa = total_willa >= meta_individual

#CARDS DE META INDIVIDUAL E STATUS POR AGENTE

st.subheader("Meta Individual e Status da Equipe")

st.markdown("""
<style>
.card {
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    font-weight: 400;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
}

.card-green {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: #e8f5e9;
}

.card-red {
    background: linear-gradient(135deg, #7f1d1d, #991b1b);
    color: #fee2e2;
}

.card-yellow {
    background: linear-gradient(135deg, #92400e, #b45309);
    color: #fff7ed;
}

.card-title {
    font-size: 22px;
    opacity: 0.9;
}

.card-value {
    font-size: 34px;
    margin-top: 6px;
}

.card-sub {
    font-size: 14px;
    margin-top: 6px;
    opacity: 0.85;
}


</style>
           
""", unsafe_allow_html=True)

col_meta, col_gab, col_lea, col_ron, col_wil = st.columns(5)

with col_meta:
    st.markdown(f"""
    <div class="card card-yellow">
        <div class="card-title">Meta Individual</div>
        <div class="card-value">{meta_individual:,}</div>
        <div class="card-sub">Meta acumulada</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

def card_agente_html(col, nome, total, status):
    classe = "card-green" if status else "card-red"
    texto = "Meta atingida" if status else "Abaixo da meta"
    with col:
        st.markdown(f"""
        <div class="card {classe}">
            <div class="card-title">{nome}</div>
            <div class="card-value">{total:,}</div>
            <div class="card-sub">{texto}</div>
        </div>
        """.replace(",", "."), unsafe_allow_html=True)

card_agente_html(col_gab, "Gabriel", total_gabriel, status_gabriel)
card_agente_html(col_lea, "Leandro", total_leandro, status_leandro)
card_agente_html(col_ron, "Rony", total_rony, status_rony)
card_agente_html(col_wil, "Willa", total_willa, status_willa)



#Criar separação visual
st.divider()
hoje = pd.Timestamp.today().normalize()
data_inicio_tabela = hoje - pd.Timedelta(days=10)
df_tabela = df[
       (df["Data"] >= data_inicio_tabela) &
       (df["Data"] <= hoje)
    ]
with st.expander("📋Ver produção diária (Últimos 10 dias)"):
   st.dataframe(df_tabela)
    

#PARA ALTERAÇÕS DO CÓDGIO:
#git add .
#git commit -m "Ajuste visual / novo KPI"
#git push
#https://dashboard-censo-equipe-m6rxxuesb5bvcaxqyd3eat.streamlit.app/
