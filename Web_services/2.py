from time import *
from datetime import *
from googlemaps import client as GoogleMaps

gmaps=GoogleMaps('AIzaSyCkwrrRzxRUVORQR9ap4m8FZUHtxkN1J5U')
lat,lng=gmaps.address_to_latlng
host_path = r"/etc/hosts"
redirect = "127.0.0.1"
websites = ["www.facebook.com", "https://www.facebook.com"]
    
while True:
    if datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9) < datetime.now() < datetime(
            datetime.now().year, datetime.now().month, datetime.now().day, 17):
        print("Working hours")

    else:
        print("Fun hours")
    sleep(5)  