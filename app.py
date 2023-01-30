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