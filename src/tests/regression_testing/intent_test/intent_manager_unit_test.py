import pytest
from unittest.mock import Mock
from src.intent_handling.cadocs_intent import CadocsIntents
from src.chatbot.intent_manager import IntentManager
import os


class TestIntentManager:

    @pytest.fixture
    def intent_manager_instance(self, mocker):
        mocker.patch('os.environ.get', return_value='mocked_nlu_url')
        intent_manager = IntentManager()
        yield intent_manager

    def test_detect_intent_info(self, mocker, intent_manager_instance):
        mock_response = {
            "intent": {
                "intent": {
                    "name": "info",
                    "confidence": 0.8
                }
            },
            "entities": {}
        }

        # Mock requests.get method
        mocker.patch('requests.get', return_value=Mock(json=lambda: mock_response))

        intent, entities, confidence, _ = intent_manager_instance.detect_intent("tell me more about community smells")

        # Assertions
        assert intent == CadocsIntents.Info
        assert entities == []
        assert confidence >= 0.8

    def test_detect_intent_get_smells(self, mocker, intent_manager_instance):
        mock_response = {
            "intent": {
                "intent": {
                    "name": "get_smells",
                    "confidence": 0.8
                }
            },
            "entities": {
                "url": "https://github.com/tensorflow/ranking"
            }
        }

        # Mock requests.get method
        mocker.patch('requests.get', return_value=Mock(json=lambda: mock_response))

        intent, entities, confidence, _ = intent_manager_instance.detect_intent(
            "can you get community smells for this repo https://github.com/tensorflow/ranking")

        # Assertions
        assert intent == CadocsIntents.GetSmells
        assert entities == ["https://github.com/tensorflow/ranking"]
        assert confidence >= 0.8

    def test_detect_intent_get_smells_date(self, mocker, intent_manager_instance):
        mocker.patch('src.chatbot.intent_manager.get_formatted_message', return_value=("dummy message", {
            "url": "https://github.com/tensorflow/ranking",
            "date": "2022/01/01"
        }))

        mocker.patch('src.chatbot.intent_manager.prediction_service.predict', return_value={
            "intent": {
                "name": "get_smells_date",
                "confidence": 0.8
            }
        })

        intent, entities, confidence, _ = intent_manager_instance.detect_intent(
            "can you get community smells for this repo https://github.com/tensorflow/ranking from 2022/01/01")

        assert intent == CadocsIntents.GetSmellsDate
        assert entities == ["https://github.com/tensorflow/ranking", "2022/01/01"]
        assert confidence >= 0.8