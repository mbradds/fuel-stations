import requests
import random

call = "http://10.0.0.128:5000/api/getRoute/Calgary,ab/London,on"

# Warm up, so you don't measure flask internal memory usage
for _ in range(10):
    requests.get(call)

# Memory usage before API calls
resp = requests.get('http://10.0.0.128:5000/api/memory')
print(f'Memory before API call {int(resp.json().get("memory"))}')

# Take first memory usage snapshot
# resp = requests.get('http://127.0.0.1:5000/snapshot')

# Start some API Calls
for _ in range(10):
    random_range = random.randint(100, 700)
    requests.put("http://10.0.0.128:5000/api/updateNetwork/ELEC/"+str(random_range)+"/CA")
    requests.get(call)
    # print("done: "+call)

# Memory usage after
resp = requests.get('http://10.0.0.128:5000/api/memory')
print(f'Memory after API call: {int(resp.json().get("memory"))}')

# Take 2nd snapshot and print result
# resp = requests.get('http://127.0.0.1:5000/snapshot')
# print(resp.text)
