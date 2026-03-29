# run_streamlit.py
# Este script é responsável por fornecer uma interface Streamlit para enviar conversas para sumarização.
# Ele utiliza AWS SQS para enviar mensagens e requer variáveis de ambiente configuradas.

import streamlit as st
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🤖 Sumarizador de Conversas Pro")
st.subheader("Envie seus dados para processamento em nuvem")

# Configuração SQS
sqs = boto3.client('sqs', region_name=os.getenv("AWS_REGION"))
queue_url = os.getenv("AWS_SQS_QUEUE_URL")

conversa = st.text_area("Cole a conversa aqui:", height=200)

if st.button("Enviar para Sumarização"):
    if conversa:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=conversa
        )
        st.success(f"✅ Enviado! ID da Mensagem: {response['MessageId']}")
        st.info("O Worker vai processar isso agora e salvar no DynamoDB.")
    else:
        st.warning("Por favor, insira algum texto.")