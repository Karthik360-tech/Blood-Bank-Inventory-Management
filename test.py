import requests 

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/donordata/'Karan'")
print("DONOR DATA [BY NAME]:")
for i in response.json() : 
    print(i ," : ", response.json()[i])

response = requests.get(BASE + "/donordata/by_id_custom/102")
print("\nDONOR DATA [BY DONOR ID]: ")
for i in response.json() : 
    print(i ," : ", response.json()[i])

response = requests.get(BASE + "/donordata/summary")
print("\nSUMMARY : ")
for i in response.json() : 
    print(i," :\n",response.json()[i])
