import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Almoxarifado", layout="wide")
st.title("📦 Sistema de Almoxarifado")

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

        # ---------------- PATRIMÔNIOS ----------------
        with aba_patrimonio:
            key_pat = f"patrimonio_df_{i}"

            arquivo_patrimonio = st.file_uploader(
                f"Planilha de patrimônios - {lab}",
                type=["xlsx", "xls"],
                key=f"upload_patrimonio_{i}"
            )

            if arquivo_patrimonio and key_pat not in st.session_state:
                st.session_state[key_pat] = pd.read_excel(arquivo_patrimonio)
                st.success("✅ Planilha de patrimônios carregada!")

            if key_pat in st.session_state:
                st.dataframe(st.session_state[key_pat], use_container_width=True)

        # ---------------- CONSUMÍVEIS ----------------
        with aba_consumiveis:
            df_key = f"consumiveis_df_{i}"
            original_key = f"consumiveis_original_{i}"

            arquivo_consumiveis = st.file_uploader(
                f"Planilha de consumíveis - {lab}",
                type=["xlsx", "xls"],
                key=f"upload_consumiveis_{i}"
            )

            if arquivo_consumiveis and df_key not in st.session_state:
                df = pd.read_excel(arquivo_consumiveis)
                st.session_state[df_key] = df.copy()
                st.session_state[original_key] = df.copy()
                st.success("✅ Planilha importada")

            if df_key in st.session_state:
                df = st.session_state[df_key]

                st.subheader("📊 Planilha em uso (editável)")
                st.dataframe(df, use_container_width=True)

                # -------- SALVAR PLANILHA --------
                st.divider()
                st.subheader("💾 Salvar planilha editada")

                buffer = io.BytesIO()
                df.to_excel(buffer, index=False)  # 👈 SEM engine
                buffer.seek(0)

                st.download_button(
                    label="⬇️ Salvar planilha atualizada",
                    data=buffer,
                    file_name=f"consumiveis_{lab.replace(' ', '_').lower()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                # -------- MENSAGEM --------
                if "msg" in st.session_state:
                    st.success(st.session_state["msg"])
                    del st.session_state["msg"]

                st.divider()
                st.subheader("📋 Movimentação de Estoque")

                item = st.selectbox(
                    "Selecione o item",
                    df["Nome"].sort_values(),
                    key=f"item_{i}"
                )

                tipo = st.radio(
                    "Tipo de movimentação",
                    ["Entrada", "Saída"],
                    key=f"tipo_{i}"
                )

                qtd = st.number_input(
                    "Quantidade",
                    min_value=1,
                    step=1,
                    key=f"qtd_{i}"
                )

                if st.button("Confirmar movimentação", key=f"btn_{i}"):
                    idx = df[df["Nome"] == item].index[0]

                    if tipo == "Entrada":
                        df.at[idx, "Quantidade"] += qtd
                        st.session_state["msg"] = "✅ Entrada confirmada"
                    else:
                        if df.at[idx, "Quantidade"] >= qtd:
                            df.at[idx, "Quantidade"] -= qtd
                            st.session_state["msg"] = "✅ Saída confirmada"
                        else:
                            st.error("❌ Quantidade insuficiente")
                            st.stop()

                    st.session_state[df_key] = df
                    st.rerun()

                with st.expander("📂 Mostrar planilha original"):
                    st.dataframe(st.session_state[original_key], use_container_width=True)
