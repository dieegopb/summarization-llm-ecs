import os

import boto3
from dotenv import load_dotenv

load_dotenv()

# Conexão com AWS Real (sem endpoint_url)

region = os.getenv("AWS_REGION", "us-east-1")
queue_url = os.getenv("AWS_SQS_QUEUE_URL")


sqs = boto3.client(
    'sqs', 
    region_name=region,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

mensagens = [
    "Ontem fui ao supermercado e percebi que muitos produtos estavam em promoção. Aproveitei para comprar frutas, verduras e alguns itens de limpeza. No caixa, encontrei uma amiga de infância e conversamos rapidamente sobre como a cidade mudou nos últimos anos. Saí de lá sentindo que o tempo passa muito rápido e que precisamos aproveitar mais os pequenos encontros do dia a dia.",
"Durante a reunião da equipe, discutimos os principais desafios do projeto e cada um pôde expor suas dificuldades. O gerente sugeriu novas estratégias para melhorar a comunicação e pediu que todos enviassem um relatório semanal com o andamento das tarefas. No final, ficou claro que, apesar dos obstáculos, todos estavam comprometidos em entregar o melhor resultado possível.", 
"No último final de semana, viajei para a casa dos meus avós no interior. A viagem foi tranquila e, ao chegar, fui recebido com um almoço delicioso. Passamos a tarde conversando na varanda, relembrando histórias antigas e rindo bastante. Antes de ir embora, prometi que voltaria mais vezes, pois esses momentos em família são realmente especiais.", 
"Sou o Diego e moro em São Paulo. Trabalho como desenvolvedor de software e adoro aprender novas tecnologias. Nos meus tempos livres, gosto de praticar esportes, especialmente futebol, e de assistir a filmes de ficção científica. Acredito que a tecnologia tem o poder de transformar vidas e estou sempre em busca de projetos que possam fazer a diferença no mundo."
]

print("-" * 50)
print(f"🚀 Enviando {len(mensagens)} mensagens para a nuvem...")
print("-" * 50)


for i, texto in enumerate(mensagens, 1):
    try:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=texto
        )
        print(f"[✓] {i}/{len(mensagens)} enviada com sucesso!")
    except Exception as e:
        print(f"[X] Erro ao enviar a {i}: {e}")

print("-" * 50)
print("✅ Sucesso! Agora mude para a janela do Docker e veja o resumo acontecer.")
print("-" * 50)