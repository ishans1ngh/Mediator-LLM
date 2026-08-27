from tests.conftest import client


def test_list_trials(client):
    response = client.get("/api/v1/trials")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_trial_by_id(client):
    response = client.get("/api/v1/trials")
    trials = response.json()
    if trials:
        trial_id = trials[0]["id"]
        response = client.get(f"/api/v1/trials/{trial_id}")
        assert response.status_code == 200
        data = response.json()
        assert "nct_id" in data
        assert "title" in data


def test_get_trial_by_nct(client):
    response = client.get("/api/v1/trials")
    trials = response.json()
    if trials:
        nct_id = trials[0]["nct_id"]
        response = client.get(f"/api/v1/trials/nct/{nct_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nct_id"] == nct_id


def test_trial_filter_by_status(client):
    response = client.get("/api/v1/trials?status=Recruiting")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_trial_search(client):
    response = client.get("/api/v1/trials?search=glioblastoma")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_trial_not_found(client):
    import uuid
    fake_id = uuid.uuid4()
    response = client.get(f"/api/v1/trials/{fake_id}")
    assert response.status_code == 404


def test_get_trial_criteria(client):
    response = client.get("/api/v1/trials")
    trials = response.json()
    if trials:
        trial_id = trials[0]["id"]
        response = client.get(f"/api/v1/trials/{trial_id}/criteria")
        assert response.status_code == 200
        data = response.json()
        assert "inclusion" in data
        assert "exclusion" in data
