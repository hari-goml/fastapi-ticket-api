import cProfile
import requests

def run():
    for _ in range(100):
        response = requests.post(
            "http://127.0.0.1:8000/tickets/",
            json={
                "title": "Login issue",
                "description": "Unable to login",
                "priority": "high",
                "status": "open"
            },
        )
        assert response.status_code == 200

cProfile.run("run()")