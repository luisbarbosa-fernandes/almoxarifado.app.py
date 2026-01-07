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

abas_labs = st.tabs(laboratorios)

for i, lab in enumerate(laboratorios):
    with abas_labs[i]:
        st.header(f"🏫 Laboratório de {lab}")

        aba_patrimonio, aba_consumiveis = st.tabs(
            ["📌 Patrimônios", "📦 Consumíveis"]
        )

        # -------------------------
        # PATRIMÔNIOS
        # -------------------------
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
                st.dataframe(df_patrimonio, use_container_width=True)

        # -------------------------
        # CONSUMÍVEIS
        # -------------------------
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

                st.dataframe(df_consumiveis, use_container_width=True)

                st.divider()
                st.subheader("📋 Movimentação de Estoque")

                lab_key = lab.replace(" ", "_")

                item = st.selectbox(
                    "Selecione o item",
                    df_consumiveis["Nome"].sort_values(),
                    key=f"item_{lab_key}"
                )

                tipo = st.radio(
                    "Tipo de movimentação",
                    ["Entrada", "Saída"],
                    key=f"tipo_{lab_key}"
                )

                quantidade = st.number_input(
                    "Quantidade",
                    min_value=1,
                    step=1,
                    key=f"qtd_{lab_key}"
                )

                if st.button("Confirmar movimentação", key=f"btn_{lab_key}"):

                    idx = df_consumiveis[df_consumiveis["Nome"] == item].index[0]

                    if tipo == "Entrada":
                        df_consumiveis.at[idx, "Quantidade"] += quantidade
                        st.success(f"✅ Entrada de {quantidade} unidades registrada")

                    else:
                        if df_consumiveis.at[idx, "Quantidade"] >= quantidade:
                            df_consumiveis.at[idx, "Quantidade"] -= quantidade
                            st.success(f"✅ Saída de {quantidade} unidades registrada")
                        else:
                            st.error("❌ Quantidade insuficiente em estoque")

                    st.divider()
                    st.subheader("📊 Estoque atualizado")
                    st.dataframe(df_consumiveis, use_container_width=True)

