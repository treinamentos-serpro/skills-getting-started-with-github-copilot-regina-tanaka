def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_available_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["max_participants"] == 12


def test_signup_adds_participant_to_activity(client):
    # Arrange
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/Soccer Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student@example.com for Soccer Club"
    assert email in client.get("/activities").json()["Soccer Club"]["participants"]


def test_signup_for_unknown_activity_returns_not_found(client):
    # Arrange

    # Act
    response = client.post("/activities/Unknown Club/signup?email=student@example.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_bad_request(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_from_unknown_activity_returns_not_found(client):
    # Arrange

    # Act
    response = client.delete("/activities/Unknown Club/unregister?email=student@example.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_not_found(client):
    # Arrange

    # Act
    response = client.delete("/activities/Chess Club/unregister?email=student@example.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"