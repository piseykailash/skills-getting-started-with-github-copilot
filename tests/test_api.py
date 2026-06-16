"""
Tests for FastAPI Activity Management API endpoints

Uses AAA (Arrange-Act-Assert) pattern for clear test structure.
"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status 200"""
        # Arrange
        # No setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary"""
        # Arrange
        # No setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert isinstance(response.json(), dict)
    
    def test_get_activities_contains_chess_club(self, client):
        """Test that activities list contains Chess Club"""
        # Arrange
        expected_activity = "Chess Club"
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert expected_activity in activities
    
    def test_get_activities_chess_club_has_required_fields(self, client):
        """Test that Chess Club activity has all required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        for field in required_fields:
            assert field in chess_club
    
    def test_get_activities_all_have_description(self, client):
        """Test that all activities have a description"""
        # Arrange
        # No setup needed
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful(self, client):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test signup for non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_email_returns_400(self, client):
        """Test signup with duplicate email returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_response_contains_message(self, client):
        """Test that signup response contains a confirmation message"""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert "message" in response.json()
        assert email in response.json()["message"]
        assert activity_name in response.json()["message"]


class TestRemoveFromActivity:
    """Test suite for DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_remove_existing_participant(self, client):
        """Test removing an existing participant from an activity"""
        # Arrange
        activity_name = "Music Ensemble"
        email = "bob@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_remove_nonexistent_activity_returns_404(self, client):
        """Test removing from non-existent activity returns 404"""
        # Arrange
        activity_name = "Fake Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_nonexistent_participant_returns_404(self, client):
        """Test removing non-existent participant returns 404"""
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
    
    def test_remove_response_contains_message(self, client):
        """Test that remove response contains a confirmation message"""
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert "message" in response.json()
        assert email in response.json()["message"]
        assert activity_name in response.json()["message"]


class TestIntegration:
    """Integration tests for signup/remove workflow"""
    
    def test_signup_then_remove_workflow(self, client):
        """Test complete signup and removal workflow"""
        # Arrange
        email = "workflow@mergington.edu"
        activity = "Tennis Club"
        
        # Act - Signup
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        signup_activities = client.get("/activities").json()
        
        # Act - Remove
        remove_response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        final_activities = client.get("/activities").json()
        
        # Assert - Signup
        assert signup_response.status_code == 200
        assert email in signup_activities[activity]["participants"]
        
        # Assert - Remove
        assert remove_response.status_code == 200
        assert email not in final_activities[activity]["participants"]
    
    def test_signup_multiple_different_activities(self, client):
        """Test signing up for multiple different activities"""
        # Arrange
        email = "multiactivity@mergington.edu"
        activities_to_join = ["Chess Club", "Art Studio", "Science Club"]
        
        # Act - Sign up for each activity
        signup_responses = []
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            signup_responses.append(response)
        
        # Act - Verify all signups
        all_activities = client.get("/activities").json()
        
        # Assert - All signups successful
        for response in signup_responses:
            assert response.status_code == 200
        
        # Assert - Email appears in all activities
        for activity in activities_to_join:
            assert email in all_activities[activity]["participants"]
