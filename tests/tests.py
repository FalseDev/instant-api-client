from typing import Dict

from httpx import Client

from apiclient import APIClient, APIRouter, Get, endpoint


class PeopleRouter(APIRouter):
    path = "/people"

    @endpoint
    def get_all_people(self, *, quantity: int) -> Dict:
        return Get("/all", params={'quantity': quantity})


class ApiTestClient(APIClient):
    base_url = "https://api.github.com"
    people: PeopleRouter


def test_request_creation():
    session = Client()
    test_client = ApiTestClient(session=session)
    request = test_client.people.get_all_people.callback(
        test_client, quantity=10)
    absolute_url = request.dict(router=test_client.people)['url']
    assert request.params == {'quantity': 10}
    assert absolute_url == "https://api.github.com/people/all"
