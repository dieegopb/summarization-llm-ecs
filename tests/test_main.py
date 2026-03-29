import unittest
from unittest.mock import patch, MagicMock
import app.main

class TestMain(unittest.TestCase):
    @patch('app.main.boto3.client')
    @patch('app.main.boto3.resource')
    @patch('app.main.TextSummarizer')
    def test_main_loop_receives_and_processes_messages(self, MockSummarizer, MockResource, MockClient):
        # Setup mocks
        mock_sqs = MagicMock()
        # First call: return one message; second call: raise StopIteration to exit loop
        mock_sqs.receive_message.side_effect = [
            {'Messages': [{'MessageId': '1', 'Body': 'texto', 'ReceiptHandle': 'abc'}]},
            StopIteration(),
        ]
        MockClient.return_value = mock_sqs
        mock_table = MagicMock()
        MockResource.return_value.Table.return_value = mock_table
        mock_summarizer = MagicMock()
        mock_summarizer.summarize.return_value = 'resumo'
        MockSummarizer.return_value = mock_summarizer

        with patch('builtins.print') as mock_print, patch('time.strftime', return_value='2026-03-29 12:00:00'), patch('time.sleep'):
            # Run until StopIteration is raised by the second call
            with self.assertRaises(StopIteration):
                app.main.main()

            mock_summarizer.summarize.assert_called()
            mock_table.put_item.assert_called()
            mock_sqs.delete_message.assert_called()

if __name__ == '__main__':
    unittest.main()
