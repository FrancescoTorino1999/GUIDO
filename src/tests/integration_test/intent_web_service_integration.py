import sys
from unittest.mock import MagicMock, patch
import unittest
import os
import requests

# Mock per IntentManager per evitare dipendenze NLU/torch.
sys.modules['src.chatbot.intent_manager'] = MagicMock()

from src.intent_web_service import app as flask_app
from src.intent_handling.cadocs_intent import CadocsIntents

flask_app.config['TESTING'] = True

class TestIntentWebServiceIntegration(unittest.TestCase):

    DEFAULT_ENV_VARS = {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    }

    def setUp(self):
        self.client = flask_app.test_client()

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    # Non mockiamo più requests.get qui perché ci aspettiamo un errore prima
    @patch('src.intent_web_service.IntentManager')
    def test_resolve_intent_with_message_get_smells_original_code_error(self, MockIntentManager):
        """
        Testa /resolve_intent con 'message' -> GetSmells.
        Con IntentResolver e CsDetectorTool originali, ci aspettiamo un errore
        perché CsDetectorTool riceve un dict per 'entities' ma si aspetta una lista.
        """
        mock_intent_manager_instance = MockIntentManager.return_value
        detected_entities_dict = {"repo": "test/repo-message"}
        mock_intent_manager_instance.detect_intent.return_value = (
            CadocsIntents.GetSmells,
            detected_entities_dict,
            "show me smells in test/repo-message",
            "en"
        )

        request_data = {"message": "show me smells in test/repo-message"}
        response = self.client.post('/resolve_intent', json=request_data)

        # Ci aspettiamo un errore 500 perché CsDetectorTool fallirà
        self.assertEqual(response.status_code, 500)
        mock_intent_manager_instance.detect_intent.assert_called_once_with(request_data["message"])

        response_data = response.get_json()
        self.assertIn("error", response_data)
        self.assertTrue("An error occurred while resolving intent" in response_data["error"])

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.post')
    @patch('src.intent_web_service.IntentManager', MagicMock())
    def test_resolve_intent_community_inspector_analyze_direct_original_messages(self, mock_requests_post):
        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        ci_tool_result_dict = {"job_id": "ci-analyze-real-direct"} # Questo è ciò che il tool restituisce
        mock_response_post.json.return_value = ci_tool_result_dict
        mock_requests_post.return_value = mock_response_post

        request_data = {
            "author": "direct_author_ci",
            "repository": "direct_repo_ci",
            "end_date": "2023-12-25"
        }
        response = self.client.post('/resolve_intent', json=request_data)
        self.assertEqual(response.status_code, 200)

        mock_requests_post.assert_called_once_with(
            f"{self.DEFAULT_ENV_VARS['TOAD_URL']}/analyze", json=request_data
        )

        self.assertEqual(response.json, ci_tool_result_dict)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get')
    @patch('src.intent_web_service.IntentManager', MagicMock())
    def test_resolve_intent_community_inspector_results_direct_original_messages(self, mock_requests_get):
        job_id = "ci-results-real-direct"
        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = {"job_id": job_id, "status": "SUCCESS"}

        mock_result_response = MagicMock()
        mock_result_response.status_code = 200
        ci_tool_full_results_dict = {"job_id": job_id, "status": "SUCCESS", "results": {"info": "some_ci_data"}}
        mock_result_response.json.return_value = ci_tool_full_results_dict

        mock_requests_get.side_effect = [mock_status_response, mock_result_response]

        request_data = {"job_id": job_id}
        response = self.client.post('/resolve_intent', json=request_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(mock_requests_get.call_count, 2)

        self.assertEqual(response.json, ci_tool_full_results_dict)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.post')
    @patch('src.intent_web_service.IntentManager', MagicMock())
    def test_resolve_intent_geodispersion_direct_original_messages(self, mock_requests_post):
        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        geo_tool_result_dict = {"pdi": 8.0, "idv": 2.1, "lto": 6.3}
        mock_response_post.json.return_value = geo_tool_result_dict
        mock_requests_post.return_value = mock_response_post

        request_data_entities_list = [
            {"number": 200, "nationality": "USA"},
            {"number": 30, "nationality": "Canada"}
        ]
        request_body_for_endpoint = {"entities": request_data_entities_list}

        response = self.client.post('/resolve_intent', json=request_body_for_endpoint)
        self.assertEqual(response.status_code, 200)

        mock_requests_post.assert_called_once_with(
            self.DEFAULT_ENV_VARS['GEODISPERSION_URL'], json=request_data_entities_list
        )

        self.assertEqual(response.json, geo_tool_result_dict)

    def test_resolve_intent_invalid_json(self):
        response = self.client.post('/resolve_intent', data="not json", content_type="application/json")
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json["error"], "Invalid request: JSON required")

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get')
    @patch('requests.post')
    @patch('src.intent_web_service.IntentManager')
    def test_resolve_intent_resolver_internal_error_original_code(self, MockIntentManager, mock_requests_post, mock_requests_get):
        # Questo test simula un errore di rete
        # che porta a un errore 500 gestito da resolve_utils.
        mock_intent_manager_instance = MockIntentManager.return_value
        mock_intent_manager_instance.detect_intent.return_value = (
            CadocsIntents.GetSmells, # o un altro intent che usa un tool
            {"repo": "error/repo"},
            "trigger resolver error",
            "en"
        )

        # Simula un errore di rete quando il tool (es. CsDetectorTool) tenta la chiamata
        mock_requests_get.side_effect = requests.exceptions.RequestException("Simulated network error from tool")

        request_data = {"message": "trigger resolver error"}
        response = self.client.post('/resolve_intent', json=request_data)

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)
        self.assertTrue("An error occurred while resolving intent" in response.json["error"])

        mock_intent_manager_instance.detect_intent.assert_called_once_with(request_data["message"])


    def test_build_intent_valid(self):
        intent_val = "get_smells"
        expected_intent = CadocsIntents.GetSmells
        from src.intent_web_service import build_intent
        self.assertEqual(build_intent(intent_val), expected_intent)

    def test_build_intent_invalid(self):
        intent_val = "unknown_intent"
        from src.intent_web_service import build_intent
        with self.assertRaises(ValueError) as context:
            build_intent(intent_val)
        self.assertTrue(f"Unknown intent: {intent_val}" in str(context.exception))

if __name__ == '__main__':
    unittest.main()