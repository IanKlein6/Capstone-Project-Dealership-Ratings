import requests
import json
from .models import CarDealer, CarMake, CarModel
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
     # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):

    try:
        response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'}, 
                                 json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    #print("\nJSON RESULT",json_result)
    print("1")
    if "dealerships" in json_result:
        print("2")
        # Get the list of dealerships from the response
        dealerships = json_result["dealerships"]
        #print(dealerships)
        for dealer in dealerships:
            print("3")
            #print(dealer)
            if "address" in dealer:
                print("4")
                dealer_doc = dealer
                # Create a CarDealer object with values from the dealer document
                dealer_obj = CarDealer(
                    address=dealer_doc.get("address"),
                    city=dealer_doc.get("city"),
                    full_name=dealer_doc.get("full_name"),
                    id=dealer_doc.get("id"),
                    lat=dealer_doc.get("lat"),
                    long=dealer_doc.get("long"),
                    short_name=dealer_doc.get("short_name"),
                    st=dealer_doc.get("st"),
                    zip=dealer_doc.get("zip")
                )
                results.append(dealer_obj)
                print(dealerships)
    return results


# def get_dealers_from_cf(url, **kwargs):
#     results = []

#     # Call get_request with a URL parameter
#     state = kwargs.get("state")
#     if state:
#         json_result = get_request(url, state=state)
#     else:
#         json_result = get_request(url)


#     if json_result:
#         # Get the row list in JSON as dealers
#         dealers = json_result
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer["doc"]
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], 
#                                    city=dealer_doc["city"], 
#                                    full_name=dealer_doc["full_name"],
#                                    id=dealer_doc["id"], 
#                                    lat=dealer_doc["lat"], 
#                                    long=dealer_doc["long"],
#                                    short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], 
#                                    zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):

# def get_dealer_by_id_from_cf(url, id):
#     json_result = get_request(url, id=id)
#     print('json_result from line 54', json_result)
#     if json_result:
#         dealers = json_result[0]
#     print("line 70 restapis",json_result)
#     dealer_doc = dealers
#     print("0th address element line 73", dealers["address"])
#     dealer_obj = CarDealer(address=dealers["address"], city=dealers["city"],id=dealers["id"], lat=dealers["lat"], long=dealers["long"], full_name=dealers["full_name"],short_name=dealers["short_name"], st=dealers["st"], zip=dealers["zip"])
#     return dealer_obj

def get_dealer_by_id_from_cf(url, id):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        print(dealers,"63")

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            if dealer_doc["id"] == id:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], 
                                       city=dealer_doc["city"], 
                                       full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], 
                                       lat=dealer_doc["lat"], 
                                       long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], 
                                       zip=dealer_doc["zip"])                    
                results.append(dealer_obj)

    return results[0]

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



