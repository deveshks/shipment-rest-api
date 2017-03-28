import requests
import random

def decomposition(i):
        while i > 0:
            n = random.randint(1, i)
            yield n
            i -= n
def generator():
    for i in range(0,1):
        shipment_name = "shipment_"+str(i)
        total_price = 0
        for j in range(0,10):
            total_price += random.randint(100,1000)
        total_price_bef = total_price/random.randint(10,100)
        segment_distances = list(decomposition(total_price))
        payload = { 
                "shipment_name":shipment_name,
                "total_price":total_price_bef,
                "segment_distances": segment_distances
            }
        requests.post('http://localhost:5000/shipment', json=payload)

#generator()
payload1 = { 
            "shipment_name":"shipment_test",
            "total_price":150,
            "segment_distances": [1.0,5.0]
        }
payload2 = { 
            "shipment_name":"shipment_test",
            "total_price":200,
            "segment_distances": [1.0,5.0]
        }
rda = requests.delete('http://localhost:5000/shipment')
print rda.text
'''rpo = requests.post('http://localhost:5000/shipment', json=payload1)
print rpo.json()
rg1 = requests.get('http://localhost:5000/shipment/shipment_test')
print rg1.text
rpu = requests.put('http://localhost:5000/shipment',json=payload2)
print rpu.text
rg2 = requests.get('http://localhost:5000/shipment/shipment_test')
print rg2.text'''
#rdp = requests.delete('http://localhost:5000/shipment/shipment_1')
#rda = requests.delete('http://localhost:5000/shipment')

