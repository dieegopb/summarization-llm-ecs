import unittest
from unittest.mock import patch, MagicMock
import test_send
import os

class TestTestSend(unittest.TestCase):
    @patch('test_send.boto3.client')
    @patch('test_send.print')
    def test_envio_mensagens(self, mock_print, mock_boto3_client):
        mock_sqs = MagicMock()
        mock_boto3_client.return_value = mock_sqs
        mock_sqs.send_message.return_value = None
        with patch.dict(os.environ, {"AWS_REGION": "us-east-1", "AWS_SQS_QUEUE_URL": "url", "AWS_ACCESS_KEY_ID": "id", "AWS_SECRET_ACCESS_KEY": "secret"}):
            # Executa o script
            test_send.sqs = mock_sqs
            for i, texto in enumerate(test_send.mensagens, 1):
                test_send.sqs.send_message(QueueUrl="url", MessageBody=texto)
            self.assertEqual(mock_sqs.send_message.call_count, len(test_send.mensagens))

if __name__ == '__main__':
    unittest.main()
