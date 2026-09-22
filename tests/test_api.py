import importlib

from fastapi.testclient import TestClient

app_module = importlib.import_module("src.app")

client = TestClient(app_module.app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    original = app_module.activities[activity_name]["participants"][:]
    app_module.activities[activity_name]["participants"] = ["alice@example.com", "bob@example.com"]

    try:
        response = client.delete(f"/activities/{activity_name}/unregister?email=alice@example.com")

        assert response.status_code == 200
        assert response.json()["message"] == "Unregistered alice@example.com from Chess Club"
        assert app_module.activities[activity_name]["participants"] == ["bob@example.com"]
    finally:
        app_module.activities[activity_name]["participants"] = original


def test_unregister_participant_missing_email_returns_404():
    activity_name = "Chess Club"
    original = app_module.activities[activity_name]["participants"][:]
    app_module.activities[activity_name]["participants"] = ["alice@example.com"]

    try:
        response = client.delete(f"/activities/{activity_name}/unregister?email=bob@example.com")

        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found in this activity"
    finally:
        app_module.activities[activity_name]["participants"] = original
