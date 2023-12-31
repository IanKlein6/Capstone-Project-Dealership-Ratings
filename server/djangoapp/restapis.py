import requests
import json
from .models import CarDealer, DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
from requests.auth import HTTPBasicAuth

# Function to make a GET request
def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    print(api_key)
    print("GET from {} ".format(url))
    
    try:
        if api_key:
            params = {
                "text": kwargs["text"],
                "version": kwargs["version"],
                "features": kwargs["features"],
                "return_analyzed_text": kwargs["return_analyzed_text"]
            }
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Function to make a POST request
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print("Something went wrong: {}".format(e))
        response = None  # Set response to None in case of an error
    return response

# Function to get a list of dealers from a Cloudant database
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)
    
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Function to get dealer details by ID from a Cloudant database
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    
    if json_result and isinstance(json_result, list) and json_result:
        dealer_doc = json_result[0]
        return CarDealer(
            address=dealer_doc["address"],
            city=dealer_doc["city"],
            full_name=dealer_doc["full_name"],
            id=dealer_doc["id"],
            lat=dealer_doc["lat"],
            long=dealer_doc["long"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"],
            zip=dealer_doc["zip"]
        )
    return None

#Function to get dealer reviews from a Cloudant database
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    
    json_result = get_request(url, id=id) if id else get_request(url)
    
    if json_result:
        data = json_result.get("data")
        reviews = data.get("docs", []) if data else []

        for dealer_review in reviews:
            review_obj = DealerReview(
                dealership=dealer_review["dealership"],
                name=dealer_review["name"],
                purchase=dealer_review["purchase"],
                review=dealer_review["review"]
            )

            # Optional fields
            review_obj.id = dealer_review.get("id")
            review_obj.purchase_date = dealer_review.get("purchase_date")
            review_obj.car_make = dealer_review.get("car_make")
            review_obj.car_model = dealer_review.get("car_model")
            review_obj.car_year = dealer_review.get("car_year")


            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)
           
    return results


def analyze_review_sentiments(text):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/70760587-a8fc-490e-bb9a-9337cb87aedc"
    api_key = "54aF_M40ZvqpJJGelENsUqwl4-xQ6ttgRKY5OTunfT5W"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    
    return(label)