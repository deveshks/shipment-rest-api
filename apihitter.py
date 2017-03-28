import requests


#POST PAYLOAD
payloadpost = {
            "shipment_name":"shipment_test",
            "total_price":150.5,
            "segment_distances": [1.0,5.0]
        }

#Put payload
payloadput = { 
            "shipment_name":"shipment_test",
            "total_price":200.75,
            "segment_distances": [2.0,3.0]
        }

#Request to delete all shipments
reqdelall = requests.delete('https://obscure-wave-96442.herokuapp.com/shipment')
print reqdelall.text

'''Output
{
  "Success": "All Shipments successfully deleted"
}'''

#Request to post shipment
reqpost = requests.post('https://obscure-wave-96442.herokuapp.com/shipment', json=payloadpost)
print reqpost.text

'''Output
{
  "Success": "Shipment with name shipment_test successfully created"
}'''

#Request to get just posted shipment
reqget1 = requests.get('https://obscure-wave-96442.herokuapp.com/shipment/shipment_test')
print reqget1.text

'''Output
{
    "cost_breakdown": [
        25.0,
        125.0
    ],
    "segment_distances": [
        1.0,
        5.0
    ],
    "shipment_name": "shipment_test",
    "total_price": 150
}
'''

#Request to update just posted shipment via put
reqput = requests.put('https://obscure-wave-96442.herokuapp.com/shipment',json=payloadput)
print reqput.text

'''Output
{
  "Success": "Shipment with name shipment_test successfully updated"
}'''

#Request to get just updated shipment
reqget2 = requests.get('https://obscure-wave-96442.herokuapp.com/shipment/shipment_test')
print reqget2.text

'''Output: updated shipment
{
    "cost_breakdown": [
        80.0,
        120.0
    ],
    "segment_distances": [
        2.0,
        3.0
    ],
    "shipment_name": "shipment_test",
    "total_price": 200
}'''

#Request to delete posted shipment
reqdel = requests.delete('https://obscure-wave-96442.herokuapp.com/shipment/shipment_test')
print reqdel.text

