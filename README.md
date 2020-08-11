# geoScreen

This is a desktop gui, which detects the user's phyisical location using the Geocoder Python api, and searches through flickr.com for wallpaper worthy images that are tagged within that location using the Flickr api and saves them to a local folder on their machine.

Alternatively, since the Geocoder api is not perfectly accurate in detecting the user's exact location and city name, the gui's main functionality is to enable users in putting in their own exact locations as an alternative option rather than the detected one of the Geocoder.

Tools used: PyQt5, Geocoder API, Flickr API (https://www.flickr.com/services/api/) ,REST Countries API (https://restcountries.eu/) , Python Pickle library
