import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os
import asyncio

# Mock imports before importing the bot
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mocking external dependencies
sys.modules['telegram'] = MagicMock()
sys.modules['telegram.ext'] = MagicMock()
sys.modules['mcp_servers.google_mcp'] = MagicMock()
sys.modules['mcp_servers.files_mcp'] = MagicMock()
sys.modules['mcp_servers.llm_bridge'] = MagicMock()
sys.modules['logs.logger'] = MagicMock()

import bots.telegram_bot as bot

class TestTelegramBot(unittest.IsolatedAsyncioTestCase):

    @patch('bots.telegram_bot.llm_bridge.query_llm')
    async def test_universal_query(self, mock_query):
        mock_query.return_value = "Resposta da IA"
        result = await bot._universal_query("Olá", "System")
        self.assertEqual(result, "Resposta da IA")
        mock_query.assert_called_once_with("Olá", "System")

    @patch('bots.telegram_bot._universal_query')
    async def test_detect_intent_general(self, mock_query):
        mock_query.return_value = '{"intent": "general", "params": {}}'
        result = await bot._detect_intent("Como vai?")
        self.assertEqual(result['intent'], 'general')

    @patch('bots.telegram_bot._universal_query')
    async def test_detect_intent_gmail(self, mock_query):
        mock_query.return_value = '{"intent": "gmail_list", "params": {}}'
        result = await bot._detect_intent("Listar meus emails")
        self.assertEqual(result['intent'], 'gmail_list')

    def test_parse_json_with_markdown(self):
        json_str = '```json\n{"intent": "test"}\n```'
        result = bot._parse_json(json_str)
        self.assertEqual(result['intent'], 'test')

    def test_is_allowed(self):
        with patch('bots.telegram_bot.ALLOWED_USER_ID', 123):
            self.assertTrue(bot._is_allowed(123))
            self.assertFalse(bot._is_allowed(456))

    @patch('bots.telegram_bot.gmail_tools.list_emails')
    async def test_handle_gmail_list(self, mock_list):
        mock_list.return_value = [{"subject": "Test", "from": "user@test.com"}]
        result = await bot._handle_gmail_list()
        self.assertIn("Test", result)
        self.assertIn("user@test.com", result)

    @patch('bots.telegram_bot.calendar_tools.get_today_schedule')
    async def test_handle_calendar_today(self, mock_schedule):
        mock_schedule.return_value = [{"titulo": "Reunião", "inicio": "2026-05-09T14:00:00"}]
        result = await bot._handle_calendar_today()
        self.assertIn("Reunião", result)
        self.assertIn("14:00", result)

    def test_add_one_hour(self):
        base = "2026-05-09T10:00:00"
        res = bot._add_one_hour(base)
        self.assertEqual(res, "2026-05-09T11:00:00")

if __name__ == '__main__':
    unittest.main()
