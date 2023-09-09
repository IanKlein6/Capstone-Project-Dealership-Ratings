import requests
import json
import logging
from .models import CarDealer, CarMake, CarModel
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
     # If argument contain API KEY
    api_key = kwargs.get("api_key")
    id = kwargs.get("id")
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
    logging.warning("This is a debug message")
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


def get_dealer_by_id_from_cf(url, id):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url, id= id)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result.get("dealerships", [])

        # For each dealer object
        for dealer_doc in dealers:
            # Ensure the ID is an integer for comparison
            if int(dealer_doc["id"]) == int(id):
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

    return results[0] if results else None


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    print(json_result,"96")
    if json_result:
        reviews = json_result["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



