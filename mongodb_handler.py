from pymongo import MongoClient
import streamlit as st
from bson.objectid import ObjectId


# MongoDB connection setup
def get_db_connection():
    #Change back to original db connection to work on local:
    #client = MongoClient(
            #"mongodb+srv://dstutz:QulJC71ClrdoSIYi@chalkboarddb.ablhj7x.mongodb.net/?retryWrites=true&w=majority&appName=chalkboardDB",
            #to use mine, get rid of X.509 and use my mongoDB string
            #tls=True,
            #tlsAllowInvalidCertificates=False
    uri = "mongodb+srv://chalkboarddb.uemagi8.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=chalkboardDB"
    client = MongoClient(
            uri,
            tls=True,
            tlsCAFile='isrgrootx1.pem',
            tlsCertificateKeyFile='client_certificate.pem',  # Change to False
    )
    db = client["chalkboard_db"]
    return db

def save_notes(subject, note_name, notes):
    db = get_db_connection()
    notes_collection = db["notes"]
    notes_data = {
        "subject": subject,
        "note_name": note_name,
        "notes": notes
    }
    notes_collection.insert_one(notes_data)
    st.success("Notes saved successfully!")

def get_notes_by_subject(subject=None):
    db = get_db_connection()
    notes_collection = db["notes"]
    if subject:
        notes = notes_collection.find({"subject": subject})
    else:
        notes = notes_collection.find()
    return list(notes)

def get_subjects():
    db = get_db_connection()
    notes_collection = db["notes"]
    subjects = notes_collection.distinct("subject")
    return subjects

def delete_note(note_id):
    db = get_db_connection()
    notes_collection = db["notes"]
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 1:
        st.success("Notes deleted successfully!")
    else:
        st.error("Error: Notes could not be deleted.")
        st.write(f"Note ID: {note_id} - Delete count: {result.deleted_count}")
