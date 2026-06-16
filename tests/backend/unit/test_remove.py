"""
Unit tests for DELETE /activities/{activity_name}/signup endpoint

Uses AAA (Arrange-Act-Assert) pattern for clear test structure.
"""
import pytest


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
