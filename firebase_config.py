import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("config/taskmanager-69d16-firebase-adminsdk-hbrip-af7bb56439.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
