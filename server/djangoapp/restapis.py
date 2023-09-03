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
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    #print("\nJSON RESULT",json_result)

    if json_result:

        # Get the list of dealerships from the response

        dealerships = json_result["dealerships"]

        for dealer in dealerships:

            if "doc" in dealer and "address" in dealer["doc"]:
                dealer_doc = dealer["doc"]
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
    return results


# def get_request(url, **kwargs):
#     print(kwargs)
#     print("GET from {} ".format(url))
#     try:
#         # Call get method of requests library with URL and parameters
#         response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        
#         status_code = response.status_code
#         print("With status {} ".format(status_code))
        
#         if status_code == 204:  # No content
#             return None  # or return [] based on your use case
#         elif status_code == 200:  # OK
#             return json.loads(response.text)
#         else:
#             # If the response code is not 200 or 204, raise an error.
#             response.raise_for_status()
            
#     except requests.RequestException as e:
#         print("Request exception occurred:", str(e))
#     except json.JSONDecodeError:
#         print("Failed to decode JSON response.")
#     except Exception as e:
#         print("An unexpected error occurred:", str(e))
#     return None


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



