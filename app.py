
import pandas as pd
import unicodedata
import re
import streamlit as st
import plotly.express as px
import os
from pathlib import Path

st.set_page_config(page_title="LNT 2025 – Sicoob Secovicred", layout="wide")

# CSS para adicionar sombra na logo
st.markdown("""
<style>
    /* Adiciona sombra sutil na logo para melhor visibilidade */
    .stApp [data-testid="stImage"] > img {
        filter: drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.3));
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header & Branding ---
col1, col2 = st.columns([1,6])
with col1:
    st.image("sicoob_logo.png", width=120)
with col2:
    st.markdown("## LNT 2025 – Demandas de Treinamento")
    st.caption("Dashboard Interativo Sicoob Secovicred")

PRIMARY = "#004F3B"   # verde profundo
ACCENT  = "#00A38C"   # teal
MUTED   = "#7FBF3F"   # verde claro

# --- Data Load ---
@st.cache_data
def load_data(path=None):
    try:
        # Se não for fornecido um caminho, procurar por arquivos Excel no diretório atual
        if path is None or not os.path.exists(path):
            excel_files = list(Path('.').glob('*.xlsx'))
            if excel_files:
                path = str(excel_files[0])
                st.info(f"Usando arquivo encontrado: {path}")
            else:
                # Criar dados de exemplo se nenhum arquivo for encontrado
                st.warning("Nenhum arquivo Excel encontrado. Usando dados de exemplo.")
                df = pd.DataFrame({
                    'Departamento': ['Comercial', 'Administrativo', 'TI', 'Financeiro'],
                    'Lotação': ['Sede', 'Agência', 'Sede', 'Agência'],
                    'Em quais conhecimentos': ['Excel avançado', 'Gestão de pessoas', 'Power BI', 'SISBR'],
                    'Que tipos de treinamentos': ['Técnico', 'Comportamental', 'Técnico', 'Técnico'],
                    'Gostaria de sugerir': ['CPA 20', 'Oratória', 'Excel VBA', 'Crédito Rural'],
                    'Que formato de treinamento': ['Online', 'Presencial', 'Híbrido', 'Presencial'],
                    'Qual o melhor período': ['Manhã', 'Tarde', 'Integral', 'Manhã'],
                    'Você sente que está preparado': ['Sim', 'Em partes', 'Não', 'Em partes']
                })
                cols = {
                    'dept': 'Departamento',
                    'site': 'Lotação',
                    'gaps': 'Em quais conhecimentos',
                    'types': 'Que tipos de treinamentos',
                    'sug': 'Gostaria de sugerir',
                    'fmt': 'Que formato de treinamento',
                    'period': 'Qual o melhor período',
                    'prep': 'Você sente que está preparado'
                }
                return df, cols
                
        df = pd.read_excel(path)
        df.columns = [re.sub(r"\s+", " ", c).strip() for c in df.columns]
        def find_col(prefix):
            for c in df.columns:
                if c.lower().startswith(prefix.lower()):
                    return c
            return None
        cols = {
            'dept': find_col('Departamento'),
            'site': find_col('Lotação'),
            'gaps': find_col('Em quais conhecimentos'),
            'types': find_col('Que tipos de treinamentos'),
            'sug':  find_col('Gostaria de sugerir'),
            'fmt':  find_col('Que formato de treinamento'),
            'period': find_col('Qual o melhor período'),
            'prep': find_col('Você sente que está preparado'),
        }
        return df, cols
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        # Retornar DataFrame vazio com colunas básicas em caso de erro
        df = pd.DataFrame(columns=['Departamento', 'Lotação'])
        cols = {k: None for k in ['dept', 'site', 'gaps', 'types', 'sug', 'fmt', 'period', 'prep']}
        return df, cols

# Procurar por arquivos Excel no diretório
excel_files = list(Path('.').glob('*.xlsx'))
default_file = str(excel_files[0]) if excel_files else None

# Permitir que o usuário selecione o arquivo
uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel", type="xlsx")
if uploaded_file is not None:
    DF, C = load_data(uploaded_file)
else:
    DF, C = load_data(default_file)

# --- Sidebar Filters ---
st.sidebar.header("Filtros")
sel_dept   = st.sidebar.multiselect("Departamento", sorted(DF[C['dept']].dropna().unique().tolist())) if C['dept'] else []
sel_site   = st.sidebar.multiselect("Lotação", sorted(DF[C['site']].dropna().unique().tolist())) if C['site'] else []
sel_period = st.sidebar.multiselect("Período", sorted(DF[C['period']].dropna().unique().tolist())) if C['period'] else []
sel_fmt    = st.sidebar.multiselect("Formato", sorted(DF[C['fmt']].dropna().unique().tolist())) if C['fmt'] else []
kw = st.sidebar.text_input("Buscar palavra-chave (ex.: SISBR, oratoria, CPA 20)")

fdf = DF.copy()
if sel_dept:   fdf = fdf[fdf[C['dept']].isin(sel_dept)]
if sel_site:   fdf = fdf[fdf[C['site']].isin(sel_site)]
if sel_period: fdf = fdf[fdf[C['period']].isin(sel_period)]
if sel_fmt:    fdf = fdf[fdf[C['fmt']].isin(sel_fmt)]

if kw:
    cols_text = [c for c in [C['gaps'], C['types'], C['sug']] if c]
    def norm(s):
        s = str(s).lower()
        return ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    mask = fdf[cols_text].fillna('').agg(' '.join, axis=1).apply(norm).str.contains(norm(kw), na=False)
    fdf = fdf[mask]

# --- KPIs ---
colA, colB, colC, colD = st.columns(4)
colA.metric("Respostas", len(fdf))
if C['prep']:
    prep_counts = fdf[C['prep']].value_counts()
    colB.metric("Preparo: Em partes", int(prep_counts.get("Em partes", 0)))
    colC.metric("Preparo: Sim", int(prep_counts.get("Sim", 0)))
    colD.metric("Preparo: Não", int(prep_counts.get("Não", 0)))

# --- Topic extraction ---
def combine_text(row):
    parts = []
    for k in ['gaps','types','sug']:
        col = C[k]
        if col:
            parts.append(str(row.get(col, '')))
    return ' '.join(parts)

fdf['__txt'] = fdf.apply(combine_text, axis=1).str.lower()
patterns = {
    'Gestão e Liderança': r'gest[ãa]o|lideran[çc]a',
    'Oratória/Comunicação': r'orat[óo]ria|comunica[çc][ãa]o|falar em p[úu]blico',
    'Inteligência Emocional': r'intelig[êe]ncia emocional|gest[ãa]o emocional',
    'Produtividade/Organização': r'produtividade|organiza[çc][ãa]o|gest[ãa]o do tempo',
    'Vendas/Negociação': r'vendas?|negocia[çc][ãa]o|prospec[çc][ãa]o|fechamento',
    'Power BI/Excel/HP12C': r'power\s*bi|excel|vba|hp\s*12c|hp12c',
    'Investimentos/CPA/CEA': r'cpa\s*20|cea|investimento|fundos?',
    'Crédito Rural': r'cr[ée]dito rural|mcr|fbb420',
    'Produtos (Previdência/Seguros/Sipag)': r'previd[êe]ncia|seguros?|sipag',
    'Sistemas (SISBR/SIGAS)': r'sisbr|sigas|sicoobnet',
    'Cobrança/Repactuação': r'cobran[çc]a|repactua[çc][ãa]o',
}

rows = []
for k, pat in patterns.items():
    rows.append({"Topico": k, "Quantidade": int(fdf['__txt'].str.contains(pat, regex=True, na=False).sum())})

topics = pd.DataFrame(rows).sort_values('Quantidade', ascending=False)

# --- Charts ---
fig1 = px.bar(topics, x='Quantidade', y='Topico', orientation='h',
              title='Demandas de Treinamento por Tema',
              color='Quantidade', color_continuous_scale=[[0, PRIMARY],[1, ACCENT]])
fig1.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig1, use_container_width=True)

if C['fmt']:
    fmt = fdf[C['fmt']].dropna().str.strip().value_counts().reset_index()
    fmt.columns = ['Formato','Quantidade']
    fig2 = px.bar(fmt, x='Formato', y='Quantidade', title='Formato de Treinamento Preferido',
                  color='Quantidade', color_continuous_scale=[[0, ACCENT],[1, PRIMARY]])
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

if C['period']:
    per = fdf[C['period']].dropna().str.strip().value_counts().reset_index()
    per.columns = ['Periodo','Quantidade']
    fig3 = px.pie(per, names='Periodo', values='Quantidade', title='Melhor Período para Treinamentos', color_discrete_sequence=[PRIMARY, ACCENT, MUTED])
    st.plotly_chart(fig3, use_container_width=True)

# --- Table of records (optional) ---
st.markdown("### Registros filtrados")
st.dataframe(fdf[[c for c in DF.columns if c]], use_container_width=True)
