import os
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Cadastro de Pacientes", page_icon="🏥", layout="centered"
)

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]

# Inicialização do estado de sessão
if "pacientes" not in st.session_state:
    if os.path.exists(ARQUIVO_CSV):
        st.session_state.pacientes = pd.read_csv(ARQUIVO_CSV)
    else:
        st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

st.title("🏥 Cadastro de Pacientes")
st.markdown("Sistema para registro rápido de atendimento na recepção.")

# Formulário de Cadastro
with st.form("form_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente*")
    idade = st.number_input(
        "Idade", min_value=0, max_value=120, value=0, step=1
    )
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
    )
    prioridade = st.slider(
        "Prioridade do atendimento (5 = Urgente)",
        min_value=1,
        max_value=5,
        value=1,
    )
    motivo = st.text_area("Motivo da consulta / observações")

    enviado = st.form_submit_button("Cadastrar", type="primary")

if enviado:
    if not nome.strip():
        st.error("Por favor, preencha o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip() if motivo else "",
        }

        # Atualiza a sessão
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha])],
            ignore_index=True,
        )

        # Salva em arquivo local (persistência local)
        st.session_state.pacientes.to_csv(ARQUIVO_CSV, index=False)

        st.success("✅ Paciente cadastrado com sucesso!")

# Exibição dos dados e Exportação
st.divider()
st.subheader("📋 Últimos Pacientes Cadastrados")

if not st.session_state.pacientes.empty:
    st.dataframe(
        st.session_state.pacientes.tail(5), use_container_width=True
    )

    # Botão de Download do CSV
    csv_data = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar CSV Completo",
        data=csv_data,
        file_name="pacientes.csv",
        mime="text/csv",
    )
else:
    st.info("Nenhum paciente cadastrado até o momento.")