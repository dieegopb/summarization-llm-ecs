import unittest
from unittest.mock import patch, MagicMock
from app.summarizer import TextSummarizer
import os

class TestTextSummarizer(unittest.TestCase):
    @patch('app.summarizer.OpenAI')
    def test_init_raises_without_api_key(self, MockOpenAI):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                TextSummarizer()

    @patch('app.summarizer.OpenAI')
    def test_init_sets_client_and_model(self, MockOpenAI):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "key", "OPENAI_MODEL": "gpt-4o-mini"}):
            summarizer = TextSummarizer()
            self.assertIsNotNone(summarizer.client)
            self.assertEqual(summarizer.model, "gpt-4o-mini")

    @patch('app.summarizer.OpenAI')
    def test_summarize_raises_on_empty(self, MockOpenAI):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "key"}):
            summarizer = TextSummarizer()
            with self.assertRaises(ValueError):
                summarizer.summarize("")

    @patch('app.summarizer.OpenAI')
    def test_summarize_returns_summary(self, MockOpenAI):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Resumo gerado"))]
        mock_client.chat.completions.create.return_value = mock_response
        MockOpenAI.return_value = mock_client
        with patch.dict(os.environ, {"OPENAI_API_KEY": "key"}):
            summarizer = TextSummarizer()
            result = summarizer.summarize("Texto de teste")
            self.assertEqual(result, "Resumo gerado")

if __name__ == '__main__':
    unittest.main()
