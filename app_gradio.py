import os
from datetime import datetime
import gradio as gr
import pandas as pd

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    # Validação simples
    if not nome or not nome.strip():
        # Retorna mensagem de aviso, mantém a tabela atual sem alterações
        df_atual = (
            pd.read_csv(ARQUIVO_CSV)
            if os.path.exists(ARQUIVO_CSV)
            else pd.DataFrame(columns=COLUNAS)
        )
        return (
            "⚠️ Por favor, informe o nome do paciente.",
            df_atual.tail(5),
            nome,
            idade,
            convenio,
            prioridade,
            motivo,
        )

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade) if idade is not None else 0,
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo.strip() if motivo else "",
    }

    novo_df = pd.DataFrame([linha])

    # Persistência em CSV
    if os.path.exists(ARQUIVO_CSV):
        novo_df.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo_df.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    df_atualizado = pd.read_csv(ARQUIVO_CSV)

    # Retorna mensagem, tabela atualizada e limpa os campos do formulário
    return (
        "✅ Paciente cadastrado com sucesso!",
        df_atualizado.tail(5),
        "",  # Reseta nome
        0,  # Reseta idade
        "Particular",  # Reseta convenio
        1,  # Reseta prioridade
        "",  # Reseta motivo
    )


# Construção da Interface
with gr.Blocks(title="Cadastro de Pacientes - Gradio") as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes (Recepção)")

    # Formatação em coluna única otimizada para mobile
    with gr.Column():
        nome = gr.Textbox(
            label="Nome do paciente", placeholder="Digite o nome completo"
        )
        idade = gr.Number(label="Idade", value=0, precision=0)
        convenio = gr.Dropdown(
            choices=[
                "Particular",
                "Unimed",
                "Bradesco Saúde",
                "SulAmérica",
                "Outro",
            ],
            value="Particular",
            label="Convênio",
        )
        prioridade = gr.Slider(
            minimum=1,
            maximum=5,
            step=1,
            value=1,
            label="Prioridade do atendimento (5 = Urgente)",
        )
        motivo = gr.Textbox(
            label="Motivo da consulta / observações",
            lines=3,
            placeholder="Sintomas, observações...",
        )

        botao = gr.Button("Cadastrar Paciente", variant="primary")

        saida_msg = gr.Textbox(label="Status do Cadastro", interactive=False)
        tabela = gr.Dataframe(
            label="Últimos 5 pacientes cadastrados", interactive=False
        )

    # Evento de clique
    botao.click(
        fn=cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela, nome, idade, convenio, prioridade, motivo],
    )

if __name__ == "__main__":
    demo.launch()