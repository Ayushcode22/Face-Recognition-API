from fastapi.testclient import TestClient
from index import app
import json
import requests

client = TestClient(app)


#def test_search_face():
	#response = client.post("http://127.0.0.1:8000/search_faces/",data={"kk":"1"},files={"file":("jb.jpg",open("jb.jpg", "rb"),"image/jpeg")})
	#assert response.status_code == 200
	#assert response.json() == {"filename": "jb.jpg"}  
	
	
#def test_get_face_info():
	#response = client.post("http://127.0.0.1:8000/get_face_info/",json={"face_id":"2"})
	#assert response.status_code == 200
	#assert response.json() == {"name": ["Name: obama2; "]}


def test_add_faces_in_bulk2():
	with open("pics.zip", "rb") as f:
		response = client.post("http://127.0.0.1:8000/add_faces_in_bulk/",files={"file": ("pics.zip", f, "application/x-zip-compressed")})
		assert response.status_code == 200
		assert response.json() ==  {"file": "pics.zip"}
		
		
def test_add_face():
	with open("jb.jpg", "rb") as f:
		response = client.post("http://127.0.0.1:8000/add_face/",files={"file": ("jb.jpg", f, "image/jpeg")})
		assert response.status_code == 200
		assert response.json() ==  {"file_name": "jb"}











