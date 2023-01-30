## Retrieve hotel images

In this tutorial we will show you how you can get images for hotels to integrate them your Python hotel application.

For that we will use the [Place Photos](https://developers.google.com/maps/documentation/places/web-service/photos) API in conjuction with the [Text Search](https://developers.google.com/maps/documentation/places/web-service/search-text) and [Place Details](https://developers.google.com/maps/documentation/places/web-service/details) APIs. 

The flow is the following:

- Call the `Text Search` API by providing the name of the hotel and its latitude/longitude to get its `place_id`. This API also provides a single photo reference per place.
- Call the `Place Details` API with the `place_id` as input to get all photo references.
- Call the `Place Photos` API to download the referenced photos and resize them as needed.

### Prerequisites
- Google API key: create an account and get your key at the Google [portal](https://developers.google.com/maps/documentation/geolocation/overview)
- Python dependences: install the libraries used with the `pip install -r requirements.txt` command

### Code 

Let's now see the code. For the example we will look for images for the `HOTEL VILLA PANTHEON` at the location `48.84917,2.34615`. In your application you can get both the hotel name and the location using the [Hotel List API](https://developers.amadeus.com/self-service/category/hotel/api-doc/hotel-list).

```python
import requests
import json

# Text Search API
def get_place_id(google_key, headers):
    hotel_name = 'HOTEL VILLA PANTHEON'
    lat_lng = '48.84917,2.34615'
    base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = '?location=' + lat_lng + '&query=' + hotel_name + '&radius=10&key=' + google_key
    url = base_url + params

    response = requests.request('GET', url, headers=headers, data={})
    json_response = json.loads(response.text)
    place_id = json_response['results'][0]['place_id']
    return place_id

# Place Details API
def place_details(google_key, headers, place_id): 
    url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id=' + place_id + '&key=' + google_key

    response = requests.request('GET', url, headers=headers, data={})
    json_response = json.loads(response.text)

    photo_references = []
    for i in range(len(json_response['result']['photos'])):
        photo_references.append(json_response['result']['photos'][i]['photo_reference']
    )
    return photo_references

# Place Photos API 
def place_photos(google_key, photo_reference): 
    url = 'https://maps.googleapis.com/maps/api/place/photo?photo_reference=' + photo_reference + '&key=' + google_key

    headers = {
    'Accept': 'image/*'
    }

    response = requests.request('GET', url, headers=headers, data={})
    print(response)

def main():
    google_key = 'GOOGLE_API_KEY'
    headers = { 'Accept': 'application/json'
            }
    place_id = get_place_id(google_key, headers)
    photo_references = place_details(google_key, headers, place_id)
    photos = place_photos(google_key, photo_references[0])

if __name__ == "__main__":
    main()
```

There are 3 functions in the code that represent the flow that we have described:

`get_place_id`: it calls the Text Search API to search for a hotel with the name `HOTEL VILLA PANTHEON` located at the latitude and longitude of `48.84917,2.34615`. For the API call we pass the Google API key, headers, and search parameters. The response is then parsed into a JSON object, and the `place_id` of the first result is returned.

`place_details`: it calls the Place Details API to retrieve details about the hotel with the given place_id. A list of photo references is returned.  

`place_photo`: this function uses the Place Photos API to retrieve a photo of the hotel using the given photo reference. For this example we pass the first photo reference, but the API can be called for all the references you get.