from unittest import TestCase, mock

from py_clubhouse import Clubhouse


class BaseTestCase(TestCase):
    def _mock_response(self, status=200, content="CONTENT", json_data=None, raise_for_status=None):
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(return_value=json_data)
        return mock_resp

    def setUp(self):
        self.clubhouse = Clubhouse("fake-token")
