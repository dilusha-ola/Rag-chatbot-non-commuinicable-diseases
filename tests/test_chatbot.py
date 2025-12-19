"""
Unit tests for chatbot logic.
Run with: pytest tests/test_chatbot.py
"""

import pytest
from src.chatbot import NCDChatbot
from unittest.mock import Mock, patch


class TestChatbotInitialization:
    """Test chatbot initialization."""
    
    @patch('src.chatbot.VectorStoreManager')
    @patch('src.chatbot.GoogleGenerativeAI')
    def test_chatbot_initialization(self, mock_llm, mock_vector):
        """Test chatbot can be initialized."""
        mock_vector_instance = Mock()
        mock_vector.return_value = mock_vector_instance
        mock_vector_instance.get_retriever.return_value = Mock()
        
        chatbot = NCDChatbot()
        assert chatbot is not None
        assert hasattr(chatbot, 'chain')


class TestChatbotQueries:
    """Test chatbot query handling."""
    
    @patch('src.chatbot.VectorStoreManager')
    @patch('src.chatbot.GoogleGenerativeAI')
    def test_ask_question_returns_string(self, mock_llm, mock_vector):
        """Test that ask_question returns a string response."""
        mock_vector_instance = Mock()
        mock_vector.return_value = mock_vector_instance
        mock_vector_instance.get_retriever.return_value = Mock()
        
        mock_llm_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        
        chatbot = NCDChatbot()
        
        with patch.object(chatbot, 'chain') as mock_chain:
            mock_chain.invoke.return_value = {"answer": "Test answer"}
            result = chatbot.ask_question("What is diabetes?")
            assert isinstance(result, str)
            assert len(result) > 0
    
    @patch('src.chatbot.VectorStoreManager')
    @patch('src.chatbot.GoogleGenerativeAI')
    def test_ask_question_with_empty_input(self, mock_llm, mock_vector):
        """Test chatbot handles empty questions."""
        mock_vector_instance = Mock()
        mock_vector.return_value = mock_vector_instance
        mock_vector_instance.get_retriever.return_value = Mock()
        
        chatbot = NCDChatbot()
        result = chatbot.ask_question("")
        assert isinstance(result, str)
