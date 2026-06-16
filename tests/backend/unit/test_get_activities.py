"""
Unit tests for GET /activities endpoint

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
