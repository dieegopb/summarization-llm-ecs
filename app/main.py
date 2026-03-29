import os
import time
import boto3
from dotenv import load_dotenv
from app.summarizer import TextSummarizer

load_dotenv()

def main():
    # Configurações
    region = os.getenv("AWS_REGION", "us-east-1")
    queue_url = os.getenv("AWS_SQS_QUEUE_URL")
    
    # Inicializa Clientes AWS
    sqs = boto3.client('sqs', region_name=region)
    # Resource é mais fácil de usar para o DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table('ResumosConversas')
    
    summarizer = TextSummarizer()

    print(f"--- [Worker de Produção Ativo] --- | Monitorando: {queue_url} | Destino: Tabela DynamoDB 'ResumosConversas'")
    
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=3,
            WaitTimeSeconds=20
        )

        messages = response.get('Messages', [])
        if not messages:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} [.] Aguardando mensagens...")
            continue

        for msg in messages:
            try:
                current_msg_id = msg['MessageId']
                body = msg['Body']
                handle = msg['ReceiptHandle']

                now = time.strftime('%Y-%m-%d %H:%M:%S')
                summary = summarizer.summarize(body)

                # Salva no DynamoDB
                table.put_item(
                   Item={
                        'id': current_msg_id,
                        'texto_original': body,
                        'resumo': summary,
                        'data_processamento': now
                    }
                )
                # Remove da fila
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=handle)

                # Log único e rastreável
                # Verde para sucesso

                print(f"MSG_PROCESSED | time={now} | id={current_msg_id} | status=ok | resumo={summary}")

            except Exception as e:
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                # Vermelho para erro
                RED = '\033[31m'
                RESET = '\033[0m'
                print(f"MSG_PROCESSED | time={now} | id={msg.get('MessageId', 'N/A')} | status=error | error={e}")


if __name__ == "__main__":
    main()