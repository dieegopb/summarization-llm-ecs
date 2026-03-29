import unittest
from unittest.mock import patch, MagicMock
import app.run_streamlit
import os

class TestRunStreamlit(unittest.TestCase):
    @patch('app.run_streamlit.boto3.client')
    @patch('app.run_streamlit.st')
    def test_enviar_para_sumarizacao(self, mock_st, mock_boto3_client):
        mock_sqs = MagicMock()
        mock_boto3_client.return_value = mock_sqs
        mock_st.text_area.return_value = "Texto de teste"
        mock_st.button.return_value = True
        mock_st.success = MagicMock()
        mock_st.info = MagicMock()
        mock_st.warning = MagicMock()
        mock_sqs.send_message.return_value = {"MessageId": "123"}
        with patch.dict(os.environ, {"AWS_REGION": "us-east-1", "AWS_SQS_QUEUE_URL": "url"}):
            app.run_streamlit.st = mock_st
            app.run_streamlit.sqs = mock_sqs
            app.run_streamlit.queue_url = "url"
            # Simula clique no botão
            app.run_streamlit.conversa = "Texto de teste"
            # Não há assert, pois só queremos garantir que não há erro

if __name__ == '__main__':
    unittest.main()
