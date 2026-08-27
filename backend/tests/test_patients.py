from tests.conftest import client


def test_create_patient(client):
    response = client.post(
        "/api/v1/patients",
        json={
            "patient_code": "PT-001",
            "name": "Test Patient",
            "age": 52,
            "gender": "Male",
            "diagnosis": "Glioblastoma",
            "disease_stage": "Grade IV",
            "clinical_notes": "Test notes",
            "medical_history": "Test history",
            "performance_status": "ECOG 1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["patient_code"] == "PT-001"
    assert data["status"] == "created"
    assert "id" in data


def test_list_patients(client):
    client.post(
        "/api/v1/patients",
        json={
            "patient_code": "PT-001",
            "name": "Test Patient",
            "age": 52,
            "diagnosis": "Glioblastoma",
        },
    )
    
    response = client.get("/api/v1/patients")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_get_patient(client):
    create_response = client.post(
        "/api/v1/patients",
        json={
            "patient_code": "PT-002",
            "name": "Test Patient 2",
            "age": 45,
            "diagnosis": "Glioblastoma",
        },
    )
    patient_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/patients/{patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_code"] == "PT-002"
    assert data["name"] == "Test Patient 2"


def test_update_patient(client):
    create_response = client.post(
        "/api/v1/patients",
        json={
            "patient_code": "PT-003",
            "name": "Test Patient 3",
            "age": 50,
            "diagnosis": "Glioblastoma",
        },
    )
    patient_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/v1/patients/{patient_id}",
        json={"age": 51, "performance_status": "ECOG 2"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == 51
    assert data["performance_status"] == "ECOG 2"


def test_delete_patient(client):
    create_response = client.post(
        "/api/v1/patients",
        json={
            "patient_code": "PT-004",
            "name": "Test Patient 4",
            "age": 55,
            "diagnosis": "Glioblastoma",
        },
    )
    patient_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/patients/{patient_id}")
    assert response.status_code == 200
    
    get_response = client.get(f"/api/v1/patients/{patient_id}")
    assert get_response.status_code == 404


def test_add_lab(client):
    create_response = client.post(
        "/api/v1/patients",
        json={
            "patient_code": "PT-005",
            "name": "Test Patient 5",
            "age": 48,
            "diagnosis": "Glioblastoma",
        },
    )
    patient_id = create_response.json()["id"]
    
    response = client.post(
        f"/api/v1/patients/{patient_id}/labs",
        json={
            "test_name": "Hemoglobin",
            "value": "12.5",
            "unit": "g/dL",
            "status": "NORMAL",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["test_name"] == "Hemoglobin"
    assert data["value"] == "12.5"


def test_add_treatment(client):
    create_response = client.post(
        "/api/v1/patients",
        json={
            "patient_code": "PT-006",
            "name": "Test Patient 6",
            "age": 60,
            "diagnosis": "Glioblastoma",
        },
    )
    patient_id = create_response.json()["id"]
    
    response = client.post(
        f"/api/v1/patients/{patient_id}/treatments",
        json={
            "treatment_name": "Temozolomide",
            "treatment_type": "Chemotherapy",
            "status": "Completed",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["treatment_name"] == "Temozolomide"
    assert data["treatment_type"] == "Chemotherapy"
