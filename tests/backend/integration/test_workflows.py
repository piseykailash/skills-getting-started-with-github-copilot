"""
Integration tests for signup/remove workflow

Uses AAA (Arrange-Act-Assert) pattern for clear test structure.
"""
import pytest


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
