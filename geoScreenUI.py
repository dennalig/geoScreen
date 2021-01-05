# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gsui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
# added widgets 
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QIcon

# Requests imports and so on
import requests
import json
import pickle
import os
#Non GUI related
import geocoder
import requests
from bs4 import *
from flickrapi import FlickrAPI
import pandas as pd
import urllib.request
import sys
import pathlib


import easygui

#TOdo ....incorporate imported libraries for object detection among pictures to remove images that have people in them
def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.request.URLError: 
        return False



api_key = str(os.environ.get('GEO_SCREEN_FLICKR_API')).encode('utf-8')
api_secret= str(os.environ.get('GEO_SCREEN_FLICKR_SECRET')).encode('utf-8')
extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
flickr = FlickrAPI(api_key, api_secret, format="utf-8")
#new valid format

FLICKR_IMAGE = \
    'https://www.flickr.com/search/?q='

# The User-Agent request header contains a characteristic string 
# that allows the network protocol peers to identify the application type, 
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

SAVE_FOLDER = 'Geo images\\' 


if not os.path.exists(SAVE_FOLDER):
    os.mkdir(SAVE_FOLDER)

save_Path = str(pathlib.Path(SAVE_FOLDER).parent.absolute())+"\Geo images"

  #class vars from geoScreen here




def saveLocationToPickle(locationStr):
    pickle.dump(locationStr, open("Geo images\\locationName.data", "wb")) #wb= write in binary
# gui interaction stuff here 

def loadLocationFromPickle():
    if os.path.exists("Geo images\\locationName.data"):
        locationName=pickle.load(open("Geo images\\locationName.data","rb"))
        return locationName
    else:
        return '' # returns empty String 

def saveCustomLocSettings(boolean):
    pickle.dump(boolean, open("Geo images\\customLocation.data","wb"))
    
def loadCustomLocSettings():
    if(os.path.exists("Geo images\\customLocation.data")):
        print(pickle.load(open("Geo images\\customLocation.data","rb")))
        return pickle.load(open("Geo images\\customLocation.data","rb"))
    else:
        return False

locationString=loadLocationFromPickle()

customLocationOn=loadCustomLocSettings() #boolean for custom location

newImagesFound=0
# print(locationString)

class Ui_MainWindow(object):
    #added class vars here 
    decision=''
    currentCountry=''




    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(696, 372)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.GeoSentenceLabel = QtWidgets.QLabel(self.centralwidget)
        self.GeoSentenceLabel.setGeometry(QtCore.QRect(190, 0, 351, 101))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.GeoSentenceLabel.setFont(font)
        self.GeoSentenceLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.GeoSentenceLabel.setTextFormat(QtCore.Qt.PlainText)
        self.GeoSentenceLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.GeoSentenceLabel.setObjectName("GeoSentenceLabel")
        self.countryCBox = QtWidgets.QComboBox(self.centralwidget)
        self.countryCBox.setGeometry(QtCore.QRect(340, 150, 125, 22))
        self.countryCBox.setObjectName("countryCBox")
        self.stateCBox = QtWidgets.QComboBox(self.centralwidget)
        self.stateCBox.setGeometry(QtCore.QRect(490, 150, 75, 22))
        self.stateCBox.setObjectName("stateCBox")
        self.cityCBox = QtWidgets.QComboBox(self.centralwidget)
        self.cityCBox.setGeometry(QtCore.QRect(200, 150, 121, 21))
        self.cityCBox.setObjectName("cityCBox")
        self.wrongLocationLabel = QtWidgets.QLabel(self.centralwidget)
        self.wrongLocationLabel.setGeometry(QtCore.QRect(190, 100, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        self.wrongLocationLabel.setFont(font)
        self.wrongLocationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.wrongLocationLabel.setObjectName("wrongLocationLabel")
        self.locationIndicatorLabel = QtWidgets.QLabel(self.centralwidget)
        self.locationIndicatorLabel.setGeometry(QtCore.QRect(210, 70, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        self.locationIndicatorLabel.setFont(font)
        self.locationIndicatorLabel.setText("")
        self.locationIndicatorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.locationIndicatorLabel.setObjectName("locationIndicatorLabel")
        self.setLocationButton = QtWidgets.QPushButton(self.centralwidget)
        self.setLocationButton.setGeometry(QtCore.QRect(310, 190, 75, 23))
        self.setLocationButton.setObjectName("setLocationButton")
        self.refreshLocationButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshLocationButton.setGeometry(QtCore.QRect(300, 250, 101, 21))
        self.refreshLocationButton.setObjectName("refreshLocationButton")
        self.saveFolderLabel = QtWidgets.QLabel(self.centralwidget)
        self.saveFolderLabel.setGeometry(QtCore.QRect(0, 310, 400, 41))
        self.saveFolderLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.saveFolderLabel.setObjectName("saveFolderLabel")

        self.bgPic = QtWidgets.QLabel(self.centralwidget)
        self.bgPic.setGeometry(QtCore.QRect(0, 0, 691, 381))
        self.bgPic.setText("")
        self.bgPic.setPixmap(QtGui.QPixmap("bg.png"))
        self.bgPic.setScaledContents(True)
        self.bgPic.setObjectName("bgPic")
        self.bgPic.raise_()
        self.GeoSentenceLabel.raise_()
        self.countryCBox.raise_()
        self.stateCBox.raise_()
        self.cityCBox.raise_()
        self.wrongLocationLabel.raise_()
        self.locationIndicatorLabel.raise_()
        self.setLocationButton.raise_()
        self.refreshLocationButton.raise_()
        self.saveFolderLabel.raise_()


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Geo-Screen", "Geo-Screen -Powered By flickr.com"))
        self.GeoSentenceLabel.setText(_translate("MainWindow", "Geo-Screen has detected your location to be:"))
        self.wrongLocationLabel.setText(_translate("MainWindow", "Not your correct location? Enter your location here:"))
        self.setLocationButton.setText(_translate("MainWindow", "Set Location"))
        self.refreshLocationButton.setText(_translate("MainWindow", "Refresh Location"))
        self.saveFolderLabel.setText(_translate("MainWindow", "SAVE FOLDER:"))
        ## added code here

        self.refreshLocationButton.clicked.connect(self.refLocButtonClicked)
        self.setLocationButton.clicked.connect(self.setLocButtonClicked)
        self.countryCombo()
        self.stateCombo()
        self.cityCBox.setEditable(True)
        self.loadCityPickle()
        #ussed to check and see if the U.S. is selected 
        self.countryCBox.currentIndexChanged.connect(self.stateCombo)
        global save_Path
        self.saveFolderLabel.setText(self.saveFolderLabel.text()+" "+save_Path)
        
        #usage of geocoder functions here
        ipLocation= self.getAddressFromIp().strip() # will need a conditional
        ipLocation=self.appendUSA(ipLocation) # we get better/ more results with USA
        global locationString #must declare as global
        global customLocationOn
        if(locationString=='' or (locationString!=ipLocation and (not customLocationOn))): # conditions to call main automatically, if no location is detected, or a change has been detected along with a turned off custom switch
            
            locationString =ipLocation
            self.main()
            saveLocationToPickle(locationString)
            saveCustomLocSettings(False)
        self.presentLocation() # should present location regardless
        #Geo coder functions end here 
        self.showBg()




    ## added code is here 
    def showBg(self):
        self.bgPic.setPixmap(QtGui.QPixmap("bg.png"))



    def countryCombo(self):
        countrAbbrev={'code':'value'}
        #printful api 
        r= requests.get('https://api.printful.com/countries', countrAbbrev)
        couJson= json.loads(r.text)
        couJson=couJson['result']  
        # print(couJson)
        for country in couJson:
            # print(country['alpha2Code'] +" ("+country['name']+")")
            self.countryCBox.addItem(country['code']+" ("+country['name']+")") #parses Json data here 
        #default item is United States maybe, maybe not
        index= self.countryCBox.findText("US (United States)", QtCore.Qt.MatchFixedString)
        self.countryCBox.setCurrentIndex(index)
        print(self.currentCountry)




    def stateCombo(self):
        if(self.countryCBox.currentText()=='US (United States)'):
            #call to only the United States in the API
            stateAbbrev={'code':'value'}
            r= requests.get('https://api.printful.com/countries', stateAbbrev)
            staJson= json.loads(r.text)
            staJson=staJson['result']
            for cou in staJson:
                if(cou['name'] == 'United States'):
                    #find the United States json Object
                    couStates=cou['states']
                    # print(couStates)
                    self.stateCBox.addItem('')
                    for state in couStates:
                        # print(state['code'])
                        self.stateCBox.addItem(state['code'])
                    ind= self.stateCBox.findText('',QtCore.Qt.MatchFixedString)
                    self.stateCBox.setCurrentIndex(ind)
                    # then we list the states 
        else:
            self.stateCBox.clear()
    

    def cityCombo(self):
        #only pre entered cities
        var=''


    

    ## we will use the all countries REST API to add all of the countries and all of the states in the comboboxes 
    def refLocButtonClicked(self):
        self.decision=''
        self.folderAlterWarning()
        # print(self.decision)
        if(self.decision=='OK'): # conditional here
            # print('Refresh Location')
            global locationString
            locationString=self.getAddressFromIp()
            locationString=self.appendUSA(locationString)
            saveLocationToPickle(locationString)
            #search new images
            self.presentLocation()# displays location
            global customLocationOn
            customLocationOn=False
            saveCustomLocSettings(customLocationOn)
            self.main()


            
        

        #show warning that Geo Images will changes all images in folder
    
    def setLocButtonClicked(self):
        self.decision=''
        self.folderAlterWarning()
        # print(self.decision)
        newCity= self.cityCBox.currentText()
        if(self.decision=='OK'): # conditional here
            # print('Set Location')
            self.saveCityToPickle(self.cityCBox.currentText())
            self.loadCityPickle()
            global locationString
            if(self.countryCBox.currentText() == "US (United States)"):
                newState=self.stateCBox.currentText()
                stateAbbrev={'code':'value'}
                r= requests.get('https://api.printful.com/countries', stateAbbrev)
                staJson= json.loads(r.text)
                staJson=staJson['result']
                for cou in staJson:
                    if(cou['name'] == 'United States'):
                        #find the United States json Object
                        couStates=cou['states']
                        # print(couStates)
                        for state in couStates:
                            if(state['code']==newState):
                                newState=state['name']
            else:
                newState="" #state case for non-US places
                
            # print(newState)
            newCountry= self.countryCBox.currentText()
            countryAbrev= newCountry[0:2].strip()
            countryAbrev=self.appendUSA(countryAbrev)
            if(newState!=""): # new State case
                locationString=newCity+", "+newState+", "+countryAbrev
            else:
                locationString=newCity+", "+countryAbrev
            #must search new images, save new location, and save city name if it is new
            saveLocationToPickle(locationString)
            self.saveCityToPickle(newCity)
            self.presentLocation()
            # print(locationString)

                    # then we list the states 
                #search json state data again
            global customLocationOn
            customLocationOn=True
            saveCustomLocSettings(customLocationOn)
            self.main()
        
            
    
    def folderAlterWarning(self):
        message= QMessageBox()
        message.setIcon(QMessageBox.Warning)
        message.setWindowTitle("Geo Images Folder may be altered.")
        message.setText("NOTE: ALL Images in 'Geo images' may be changed.")

        message.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        message.setDefaultButton(QMessageBox.Cancel)
        message.buttonClicked.connect(self.popup_button)
        x= message.exec_()



    
    def popup_button(self, i):
        self.decision=i.text()



    def saveCityToPickle(self,city):
        city=city.strip() # remove every letter 
        city=city.title() #capitalize every word
        city=city.replace(","," ") # remove hazardous commas 
        savedCities=self.loadCityPickle()
        # print(savedCities)
        cityList=savedCities.split(',') # separate by comma
        cityAlreadySaved=False # so we dont have the same cities inside

        for town in cityList: 
            # print(town)
            if(town==city):
                cityAlreadySaved=True
        if(not cityAlreadySaved): # it will be saved as a text string of cities separated by a comma NOT Space (ie New York, New Delhi)
            cityString= savedCities+","+city
            pickle.dump(cityString, open("Geo images\\cities.data",'wb'))


    def loadCityPickle(self):
        if os.path.exists("Geo images\\cities.data"):
            self.cityCBox.clear()
            currentCities= pickle.load(open("Geo images\\cities.data","rb"))
            # print(currentCities)
            loadedCities=currentCities.split(',')
            for lCity in loadedCities:
                self.cityCBox.addItem(lCity.strip())
            return currentCities
        else:
            return ''



    #GEO-Screen Functions

    def getAddressFromIp(self): # geocoder api
        g= geocoder.ip('me')
        jsonData=g.geojson
        features= jsonData['features']
        addressJson=jsonData
        for x in features:
             addressJson= x['properties']
#    print(addressJson)
        addressName=addressJson['address'] # city we are to search
        # print(addressName)
        return addressName




    def presentLocation(self):
        global locationString
        self.locationIndicatorLabel.setText(locationString)
        self.locationIndicatorLabel.setStyleSheet('color: blue')
    
    def main(self): # makes if not already created
        self.search_images()
    def search_images(self):
        global locationString
        data=locationString
        print(locationString)
        # print('Starts Searching')
        global FLICKR_IMAGE
        searchUrl= FLICKR_IMAGE +data
        searchUrl=searchUrl.strip()
        searchUrl=searchUrl.replace(", ","%20")
        # print(searchUrl)
        response = requests.get(searchUrl, headers=usr_agent)
        # print(response.status_code)

        strData=str(data)
        strData=strData.replace(", "," ")
        # print(strData)

        photos=flickr.photos.search(text=strData,extras=extras)

        self.generateJson(photos)

    def generateJson(self, jsonVar):
        self.deleteAllLocationPics()
        # print(jsonVar)
        photos= jsonVar['photos']
        pagePhoto=photos['photo']

        validUrls= [] #url list, we store valid sizes into the list and then save 
        self.showLoadingMsg() #warning msg to user of the length
        counter=0 #counter to determine the name of the file.
        for x in pagePhoto:
            # print(x) # Shows gathered info of all images from location string 
            if('height_l' in x and 'width_l' in x):
                height=int(x['height_l'])
                width=int(x['width_l'])
                if(height>= 683 and width >= 1024):
                    # print(str(height)+" "+ str(width) + " "+ x['url_l'])
                    
                    url= x['url_l']
                    validUrls.append(url)
        # print('printing urls...')
        # we make a list of urls then convert from url to jpg
        for url in validUrls:
            counter+=1
            self.url_to_jpg(url,'geo-pic #', counter)
            # print(url)

        

        # self.url_to_jpg(url,'geolock', counter)
            # we stoped here:
            # python parameter explanation:  https://joequery.me/code/flickr-api-image-search-python/
            # flickr api page explanation :https://www.flickr.com/services/api/explore/flickr.photos.search
            # api key, : https://www.flickr.com/services/apps/create/noncommercial/?

#parameters.... url, string, int index
    def url_to_jpg(self,url, file_name,i):
        SAVE_FOLDER = 'Geo images\\' +file_name +str(i)+'.jpg'
        urllib.request.urlretrieve(url, SAVE_FOLDER)



   
    def deleteAllLocationPics(self): # deletes all jpgs in desired folder, so we dont have a crossover of places
        global SAVE_FOLDER
        fileList= [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".jpg")]
        for f in fileList:
            os.remove(os.path.join(SAVE_FOLDER,f))
    def showLoadingMsg(self):
        msg= QMessageBox()
        msg.setWindowTitle("Scanning Flickr.")
        global locationString
        msg.setText("Please be patient, we are now scanning flickr.com for expressive images tagged near you! The window may take several moments to be responsive. :-)")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def appendUSA(self, ipString):
        if(ipString[len(ipString)-2:]=='US'): # we get better/ more results with USA
            ipString=ipString+'A'
            return ipString
        else:
            ipString


if __name__ == "__main__":
    import sys
    internet=internet_on() # testing for internet
    if(internet):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        app_icon = QtGui.QIcon()
        app_icon.addFile('locationIcon.ico', QtCore.QSize(16,16))
        # app.setWindowIcon(QtGui.QIcon(app_icon))
        # MainWindow.setWindowIcon(QtGui.QIcon(app_icon))
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
    
        sys.exit(app.exec_())
    else:
        easygui.msgbox("In order for Geo-Screen to function, please connect to the Internet.", title="Please Connect to the Internet.")
        print("No internet.")
