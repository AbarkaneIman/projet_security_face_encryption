
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyD9uvqpgIH9axmQjETmqYStx3GSuSn9BT8",
    "authDomain": "faceencryption.firebaseapp.com",
    "databaseURL": "https://faceencryption-default-rtdb.firebaseio.com/",  # à modifier si besoin
    "projectId": "faceencryption",
    "storageBucket": "faceencryption.firebasestorage.app",
    "messagingSenderId": "880368773477",
    "appId": "1:880368773477:web:1c49838f945dca0086598c",
    "measurementId": "G-23ZL54T1L6"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
