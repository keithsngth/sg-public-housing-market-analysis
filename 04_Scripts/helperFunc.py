import requests
import numpy
import pandas as pd # For normalizing json data

# This function assumes that the dataset provided by HDB on data.gov.sg is complete and there exists records in OneMap
# The function skips checking response status and whether there are valid results (sometimes there might be duplicates or no records, causing errors downstream)

def get_coordinates(array):
    """
    Returns the geocoordinates in latitude and longitude of HDB addresses through geocoding via OneMap API.

    Args:
        array (numpy array or list): An array containing the string addresses of HDB units.

    Returns:
        coordinates_dict (dictionary): A dictionary of geocoordinates for each address.
    """
    # Create empty dictionary
    coordinates_dict = {}

    # URL for API call
    url = 'https://www.onemap.gov.sg/api/common/elastic/search'
    
    # Iterate through array to geocode each address
    for i in array:
        
        # Define API parameters
        params = {'searchVal': i,
            'returnGeom': 'Y',
            'getAddrDetails': 'Y'}
        
        # API call, include try-except to catch potential errors
        try:
            response = requests.get(url, params=params)
            response_dict = response.json()
            results = response_dict['results']
            df_temp = pd.json_normalize(results)

            coordinates_dict[i] = {'latitude': float(df_temp['LATITUDE'][0]), 'longitude': float(df_temp['LONGITUDE'][0])}

        # If error encountered during API call, return NaN
        except:
            coordinates_dict[i] = {'latitude': np.nan, 'longitude': np.nan}

    # Return dictionary of latitude and longitude for each address
    return coordinates_dict