"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
import os
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        Dict: Dictionary containing the list of databases or an error message
    """
    try:
        client = Cloudant.iam(
            account_name=param_dict["account_name"],
            api_key=param_dict["api_key"],
            connect=True,
        )
        return {"dbs": client.all_dbs()}
    except CloudantException as cloudant_exception:
        print("Unable to connect to Cloudant.")
        return {"error": str(cloudant_exception)}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("Connection error.")
        return {"error": str(err)}

if __name__ == "__main__":
    # Fetch environment variables for Cloudant account name and API key
    ACCOUNT_NAME = os.environ.get('CLOUDANT_ACCOUNT_NAME')
    API_KEY = os.environ.get('CLOUDANT_API_KEY')

    if not ACCOUNT_NAME or not API_KEY:
        print("Ensure CLOUDANT_ACCOUNT_NAME and CLOUDANT_API_KEY environment variables are set.")
        exit(1)

    param_dict = {
        "account_name": ACCOUNT_NAME,
        "api_key": API_KEY
    }
    print(main(param_dict))
