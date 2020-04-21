# import requests
# API_URL = "http://127.0.0.1:5000/api/"
# # All jobs:
# print(requests.get(API_URL + "users").json())
# # Correct create user:
# data1 = {
#     "id": 1100,
#     'team_leader': 1,
#     'job': 'samsung',
#     'work_size': '1',
#     'collaborators': '2',
#     'is_finished': False,
#     'start_date': 123,
# }
# print(requests.post(API_URL + 'users', json=data1).json())
# # Existing id:
# data2 = {
#     "id": 1000,
#     'team_leader': 1,
#     'job': 'samsung',
#     'work_size': '1',
#     'collaborators': '2',
#     'is_finished': False,
# }
# print(requests.post(API_URL + 'users', json=data2).json())
# # Missing required fields (['job']):
# data3 = {
#     'team_leader': 1,
#     'work_size': '1',
#     'collaborators': '2',
#     'is_finished': False,
# }
# print(requests.post(API_URL + 'users', json=data3).json())
# # Empty request body:
# data4 = {
# }
# print(requests.post(API_URL + 'users', json=data4).json())
# # All jobs:
# print(requests.get(API_URL + "users").json())


import requests


# Edit job with id: 333:
data2 = {
    'city_from': 'rjbnrelonboer',
}
print(requests.put("http://127.0.0.1:5000/api/" + "users/2", json=data2).json())
