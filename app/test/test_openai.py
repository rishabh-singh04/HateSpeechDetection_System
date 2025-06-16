# app/tests/test_openai_client.py

import pytest
from unittest.mock import MagicMock, patch, Mock
import os
from app.utils.openai_client import OpenAIClient

@pytest.fixture
def mock_azure_openai():
    with patch('app.utils.openai_client.AzureOpenAI') as mock:
        # Create a fully mocked client with chat.completions structure
        mock_client = MagicMock()
        mock_client.chat = MagicMock()
        mock_client.chat.completions = MagicMock()
        mock.return_value = mock_client
        yield mock

@pytest.fixture
def mock_env(monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("OPENAI_ENDPOINT", "https://test-endpoint.openai.azure.com")
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key-12345")

def test_openai_client_initialization(mock_azure_openai, mock_env):
    # Create instance
    client = OpenAIClient()
    
    # Verify AzureOpenAI was initialized correctly
    mock_azure_openai.assert_called_once_with(
        api_version="2023-12-01-preview",
        azure_endpoint="https://test-endpoint.openai.azure.com",
        api_key="test-api-key-12345"
    )

def test_ask_method(mock_azure_openai, mock_env):
    # Setup complete mock response structure
    mock_response = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Mocked response"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    # Configure mock client
    mock_client = mock_azure_openai.return_value
    mock_client.chat.completions.create.return_value = mock_response
    
    # Test the ask method
    client = OpenAIClient()
    response = client.ask("Test prompt")
    
    # Verify API call was made correctly
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful content moderation assistant."},
            {"role": "user", "content": "Test prompt"}
        ],
        temperature=0.2,
        max_tokens=200
    )
    
    # Verify response
    assert response == "Mocked response"

def test_chat_property(mock_azure_openai, mock_env):
    # Configure mock client
    mock_client = mock_azure_openai.return_value
    mock_chat = MagicMock()
    mock_client.chat = mock_chat
    
    # Test the chat property
    client = OpenAIClient()
    assert client.chat == mock_chat

def test_missing_environment_variables(mock_azure_openai):
    # Test missing OPENAI_ENDPOINT
    with patch.dict('os.environ', {}, clear=True):
        with patch('app.utils.openai_client.AzureOpenAI') as mock:
            mock.side_effect = Exception("OPENAI_ENDPOINT not found")
            with pytest.raises(Exception) as excinfo:
                OpenAIClient()
            assert "OPENAI_ENDPOINT not found" in str(excinfo.value)
    
    # Test missing OPENAI_API_KEY
    with patch.dict('os.environ', {"OPENAI_ENDPOINT": "test-endpoint"}, clear=True):
        with patch('app.utils.openai_client.AzureOpenAI') as mock:
            mock.side_effect = Exception("OPENAI_API_KEY not found")
            with pytest.raises(Exception) as excinfo:
                OpenAIClient()
            assert "OPENAI_API_KEY not found" in str(excinfo.value)

def test_api_error_handling(mock_azure_openai, mock_env):
    # Configure mock to raise exception
    mock_client = mock_azure_openai.return_value
    mock_client.chat.completions.create.side_effect = Exception("Mocked API Error")
    
    # Test error handling
    client = OpenAIClient()
    with pytest.raises(Exception) as excinfo:
        client.ask("Test prompt")
    assert "Mocked API Error" in str(excinfo.value)