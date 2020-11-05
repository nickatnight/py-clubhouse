import json
from unittest import mock

from py_clubhouse import __version__
from tests import BaseTestCase


def test_version():
    assert __version__ == "0.1.2"


class PyClubhouseTestCase(BaseTestCase):
    @mock.patch("py_clubhouse.core.request.requests.get")
    def test_get_story(self, mock_get):
        with open("tests/data/story.json") as f:
            data = json.load(f)
        mock_get.return_value = self._mock_response(status=200, json_data=data)
        story = self.clubhouse.get_story(123)

        # TODO: add more asserts as model data becomes available
        assert story.branches[0].name == "jerry"
        assert story.comments[0].text == "jerry just jinxed jennifer"
        assert story.comments[0].story_id == story.id
        assert story.commits[0].message == "John 3:16"
        assert story.external_tickets[0].id == "12345678-9012-3456-7890-123456789012"
        assert story.files[0].description == "jimmy joined jerry"
        assert story.labels[0].archived
        assert story.linked_files[0].size == 123
        assert story.pull_requests[0].branch_name == "Jill-jingles-Jans-jacket"
        assert story.stats.num_related_documents == 123
        assert story.story_links[0].object_id == 123
        assert story.tasks[0].complete

    @mock.patch("py_clubhouse.core.request.requests.get")
    def test_get_workflows(self, mock_get):
        mock_get.return_value = self._mock_response(
            status=200,
            json_data=[{"description": "foo", "states": [{"color": "bar", "name": "baz", "num_stories": 3}]}],
        )
        workflows = self.clubhouse.workflows()

        assert workflows[0].description == "foo"
        assert workflows[0].states[0].color == "bar"
        assert workflows[0].states[0].name == "baz"
        assert workflows[0].states[0].num_stories == 3

    @mock.patch("py_clubhouse.core.request.requests.get")
    def test_search_stories(self, mock_get):
        with open("tests/data/story.json") as f:
            data = json.load(f)
        mock_get.return_value = self._mock_response(
            status=200,
            json_data={"next": None, "data": [data], "total": 1},
        )
        stories = self.clubhouse.search_stories("some query")

        assert stories[0].id == 123
        assert len(stories) == 1
