import streamlit as st
import pandas as pd

st.set_page_config(page_title="Almoxarifado", layout="wide")

st.title("📦 Sistema de Almoxarifado")

# Lista dos laboratórios
laboratorios = [
    "Sistemas Digitais",
    "Eletrotécnica",
    "Instalações",
    "Energias",
    "Máquinas"
]

# abas principais
abas_labs = st.tabs(laboratorios)

for i, lab in enumerate(laboratorios):
    with abas_labs[i]:
        st.header(f"🏫 Laboratório de {lab}")

        # abas secundarias
        aba_patrimonio, aba_consumiveis = st.tabs(
            ["📌 Patrimônios", "📦 Consumíveis"]
        )

        # ---------- PATRIMÔNIOS ----------
        with aba_patrimonio:
            st.subheader("Importar planilha de patrimônios")

            arquivo_patrimonio = st.file_uploader(
                f"Planilha de patrimônios - {lab}",
                type=["xlsx", "xls"],
                key=f"patrimonio_{i}"
            )

            if arquivo_patrimonio:
                df_patrimonio = pd.read_excel(arquivo_patrimonio)
                st.success("✅ Planilha de patrimônios carregada!")
                st.dataframe(df_patrimonio)

        # ---------- CONSUMÍVEIS ----------
        with aba_consumiveis:
            st.subheader("Importar planilha de consumíveis")

            arquivo_consumiveis = st.file_uploader(
                f"Planilha de consumíveis - {lab}",
                type=["xlsx", "xls"],
                key=f"consumiveis_{i}"
            )

            if arquivo_consumiveis:
                df_consumiveis = pd.read_excel(arquivo_consumiveis)
                st.success("✅ Planilha de consumíveis carregada!")
                st.dataframe(df_consumiveis)