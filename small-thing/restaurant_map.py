__doc__ = """
Viết script tìm 50 quán bia / quán nhậu / quán bar / nhà hàng
quanh toạ độ của lớp học (lên google map để lấy) với bán kính 2KM.
Ghi kết quả theo định dạng JSON vào file pymi_beer.geojson
Sử dụng Google Map API
https://developers.google.com/places/web-service/
"""

import requests
import json
import time
import os

file_path = os.path.dirname(__file__)
with open(os.path.join(file_path, 'api_key.txt'), 'rt') as f:
    api_key = f.read()
nearby_api = (
    "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    "location={},{}&radius={}&type={}&"
    "keyword={}&key={}&language=vi"
)
detail_api = (
    "https://maps.googleapis.com/maps/api/place/details/json?"
    "place_id={}&fields=name,formatted_address,formatted_phone_number"
    "&key={}"
)
loction_api = ("https://maps.googleapis.com/maps/api/place/textsearch/json?"
               "query=71%20Nguyen%20Tat%20Thanh%20Buon%20Ma%20Thuot%20Dak%"
               "20Lak%20Viet%20Nam&key={}")

location_ses = requests.Session()
location_res = location_ses.get(loction_api.format(api_key), timeout=3)

location_data = location_res.json()
location_lat = location_data['result']["geometry"]["location"]["lat"]
location_lng = location_data['result']["geometry"]["location"]["lng"]


def nearby_search(lat, lng, radius, s_type, key_words):
    nearby_ses = requests.Session()
    detail_ses = requests.Session()
    nearby_resp = nearby_ses.get(
        nearby_api.format(lat, lng, radius,
                          s_type, ",".join(key_words), api_key),
        timeout=1
    )
    nearby_data = nearby_resp.json()

    list_place = []
    number = 1
    while True:
        for place in nearby_data['results']:
            if number <= 50:
                detail_resp = detail_ses.get(
                    detail_api.format(place['place_id'], api_key),
                    timeout=1
                )
                detail_data = detail_resp.json()
                try:
                    list_place.append(
                        dict(type="Feature", properties={
                            "name": detail_data['results']['name'],
                            "adress":
                                detail_data['results']['formatted_address'],
                            "phone":
                                detail_data['results']["formatted_phone_number"]
                        }, geometry={
                            "type": "Point",
                            "coordinates":
                                [place["geometry"]["location"]["lng"],
                                 place["geometry"]["location"]["lat"]]
                        }))
                except KeyError:
                    list_place.append(
                        dict(type="Feature", properties={
                            "name": detail_data['results']['name'],

                        }, geometry={
                            "type": "Point",
                            "coordinates":
                                [place["geometry"]["location"]["lng"],
                                 place["geometry"]["location"]["lat"]]
                        }))
            number += 1
        if "next_page_token" in nearby_data:
            time.sleep(3)
            nearby_resp = nearby_ses.get(nearby_api.format(
                lat, lng, radius, s_type, key_words, api_key)
                                         + "&pagetoken={}".format(nearby_data['next_page_token'])
                                         )
            nearby_data = nearby_resp.json()
        else:
            break
    return list_place


def export_geojson(list_place):
    data = {"type": "FeatureCollection", "features": list_place}
    with open("search.geojson", 'wt', encoding="utf8") as f_geojson:
        json.dump(data, f_geojson, indent=4)
    print("Sucess export")


def main():
    lat = location_lat
    lng = location_lng
    radius = "2000"
    keywords = ['quán nhậu', 'quán bia', 'quán bar']

    restaurant = nearby_search(lat, lng, radius, type, keywords)
    export_geojson(restaurant)


if __name__ == '__main__':
    main()
