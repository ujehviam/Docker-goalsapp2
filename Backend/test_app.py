import pytest
from unittest.mock import patch
from app import app  # Import your Flask app

@pytest.fixture
def client():
    """Create a Flask test client for sending requests."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------- Test GET /api/goals ----------
@patch("app.get_goal")
def test_get_goals(mock_get_goals, client):
    mock_get_goals.return_value = [
        {"id": 1, "goal": "Learn Flask"},
        {"id": 2, "goal": "Build API"},
    ]

    response = client.get("/api/goals")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["goal"] == "Learn Flask"


# ---------- Test POST /api/goals ----------
@patch("app.add_goal")
def test_add_goal_success(mock_add_goal, client):
    response = client.post("/api/goals", json={"goal": "Test Goal"})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Goal added!"
    mock_add_goal.assert_called_once_with("Test Goal")


@patch("app.add_goal")
def test_add_goal_missing_field(mock_add_goal, client):
    response = client.post("/api/goals", json={})

    assert response.status_code == 400
    assert "error" in response.get_json()
    mock_add_goal.assert_not_called()


# ---------- Test DELETE /api/goals/<id> ----------
@patch("app.delete_goal")
def test_delete_goal(mock_delete_goal, client):
    response = client.delete("/api/goals/1")

    assert response.status_code == 200
    assert "Goal 1 deleted!" in response.get_json()["message"]
    mock_delete_goal.assert_called_once_with(1)


# ---------- Test Error Handling ----------
@patch("app.get_goals", side_effect=Exception("DB Error"))
def test_get_goals_error(mock_get_goals, client):
    response = client.get("/api/goals")

    assert response.status_code == 500
    assert "error" in response.get_json()
    assert "DB Error" in response.get_json()["error"]