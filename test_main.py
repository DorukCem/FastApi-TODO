from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
   response = client.get("/")
   assert response.status_code == 200
   assert response.json() == {"message": "welcome"}

def test_add_todo():
   new_todo = {"name": "Test Todo"}
   response = client.post("/add-todo", json=new_todo)
   assert response.status_code == 200
   assert response.json() == {"message": "Added todo: Test Todo"}

def test_toggle_todo():
   todo_name = "Test Todo"
   response = client.post("/toggle-todo/{todo}?todo_name=Test%20Todo")
   assert response.status_code == 200
   assert response.json() == {todo_name: "True"}

def test_remove_todo():
   todo_name = "Test Todo"
   response = client.delete("/remove-todo/{todo}?todo_name=Test%20Todo")
   assert response.status_code == 200
   assert response.json() == {"message": f"Removed {todo_name}"}