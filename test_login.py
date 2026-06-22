import requests

url = "http://localhost:9016/loginTest"
data = {
    "username": "testuser5",
    "password": "testpass"
}
Authorization_header = "Bearer <token>"
response = requests.get(url, json=data, headers={"Authorization": Authorization_header})
print(response.status_code)
print(response.text)