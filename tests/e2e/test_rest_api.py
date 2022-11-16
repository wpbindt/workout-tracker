import pytest
import requests


@pytest.mark.asyncio
async def test_api(fixture_server: str) -> None:
    base_url = fixture_server + '/api'

    response = requests.post(
        base_url + '/exercise',
        json={
            'name': 'Some exx',
            'description': 'buh boh',
            'difficulty_unit': 'kg',
            'rep_unit': 'second',
        }
    )
    response.raise_for_status()

    response = requests.get(base_url + '/exercise').json()

    assert len(response) == 1
    assert response[0].get('name') == 'Some exx'
