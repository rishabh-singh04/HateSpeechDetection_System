# # app/test/test_decorators.py
# import pytest
# from unittest.mock import MagicMock, patch
# from app.utils.decorators import handle_errors, export_moderation_results
# from datetime import datetime
# import logging

# @pytest.fixture
# def mock_moderation_response():
#     # Create a mock with proper timestamp format
#     mock = MagicMock()
#     mock.action = "remove"
#     mock.classification = "hate"
#     mock.reasoning = "Contains hate speech"
#     mock.timestamp = datetime.now().isoformat()  # Convert to ISO format string
#     return mock

# def test_export_moderation_results_success(mock_moderation_response):
#     mock_func = MagicMock(return_value=mock_moderation_response)
#     decorated = export_moderation_results(mock_func)
    
#     with patch("app.data.exports.moderation_exports.ModerationExporter") as mock_exporter:
#         result = decorated("test text", None)
#         assert result == mock_moderation_response
#         mock_exporter.return_value.export_results.assert_called_once()

# def test_export_moderation_results_export_failure(caplog, mock_moderation_response):
#     mock_func = MagicMock(return_value=mock_moderation_response)
#     decorated = export_moderation_results(mock_func)
    
#     with patch("app.data.exports.moderation_exports.ModerationExporter") as mock_exporter:
#         mock_exporter.return_value.export_results.side_effect = Exception("Export failed")
#         result = decorated("test text", None)
#         assert "Export failed" in caplog.text
#         assert result == mock_moderation_response

# def test_handle_errors_success():
#     @handle_errors(default_return="default")
#     def test_func():
#         return "success"
    
#     assert test_func() == "success"

# def test_handle_errors_exception(caplog):
#     @handle_errors(default_return="default")
#     def test_func():
#         raise ValueError("error")
    
#     result = test_func()
#     assert result == "default"
#     assert "Error in test_func" in caplog.text
# app/test/test_decorators.py
# app/test/test_decorators.py
import pytest
from unittest.mock import MagicMock, patch
from app.utils.decorators import handle_errors, export_moderation_results
from datetime import datetime
import logging

@pytest.fixture
def mock_moderation_response():
    mock = MagicMock()
    mock.action = "remove"
    mock.classification = "hate"
    mock.reasoning = "Contains hate speech"
    mock.timestamp = datetime.now().isoformat()
    return mock

def test_export_moderation_results_success(mock_moderation_response):
    mock_func = MagicMock(return_value=mock_moderation_response)
    
    # Mock the entire exporter path
    with patch('app.utils.decorators.ModerationExporter') as mock_exporter_class:
        # Mock the instance methods
        mock_exporter_instance = MagicMock()
        mock_exporter_class.return_value = mock_exporter_instance
        
        decorated = export_moderation_results(mock_func)
        result = decorated("test text", None)
        
        assert result == mock_moderation_response
        mock_exporter_instance.export_results.assert_called_once()

def test_export_moderation_results_export_failure(caplog, mock_moderation_response):
    mock_func = MagicMock(return_value=mock_moderation_response)
    
    with patch('app.utils.decorators.ModerationExporter') as mock_exporter_class:
        mock_exporter_instance = MagicMock()
        mock_exporter_class.return_value = mock_exporter_instance
        mock_exporter_instance.export_results.side_effect = Exception("Export failed")
        
        decorated = export_moderation_results(mock_func)
        result = decorated("test text", None)
        
        assert "Export failed" in caplog.text
        assert result == mock_moderation_response

def test_handle_errors_success():
    @handle_errors(default_return="default")
    def test_func():
        return "success"
    assert test_func() == "success"

def test_handle_errors_exception(caplog):
    @handle_errors(default_return="default")
    def test_func():
        raise ValueError("error")
    result = test_func()
    assert result == "default"
    assert "Error in test_func" in caplog.text