import firebase_admin
from firebase_admin import credentials, firestore, db, storage
import os

#SECTION - Firebase Manager

class FireBase():
    cred = credentials.Certificate("source/fw-comm-firebase-adminsdk-qgb36-f14835ee40.json")
    firebase_admin.initialize_app(cred)

    firebase_admin.initialize_app(cred, options={
        'databaseURL': os.getenv('RealTimeDBEURL')
    }, name='realtime')

    firebase_admin.initialize_app(cred, options={
        'storageBucket': os.getenv('StorageDBURL')
    }, name='storage')

    DB_fs = firestore.client()
    DB_rtdb = db.reference(app=firebase_admin.get_app(name='realtime'))
    Storage = storage.bucket(app=firebase_admin.get_app(name='storage'))

#!SECTION
class Objetos_firebase(FireBase):
    @classmethod
    def objeto_firestore(cls):
        return cls.DB_fs
    @classmethod
    def objeto_realtimedb(cls):
        return cls.DB_rtdb
    @classmethod
    def objeto_storage(cls):
        return cls.Storage