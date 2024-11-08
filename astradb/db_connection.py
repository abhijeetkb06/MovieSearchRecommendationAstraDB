from astrapy import DataAPIClient
from astrapy.info import CollectionVectorServiceOptions
import streamlit as st

client_astra = None
db = None
collection = None

def connect_to_astra():
    """Connect to Astra DB and initialize the collection."""
    global client_astra, db, collection
    if client_astra is None or db is None or collection is None:
        try:
            client_astra = DataAPIClient("Put Astra Connection Keys here")
            db = client_astra.get_database("https://f2b8d2f5-25a4-4226-b0e8-eba94ab6181c-us-east-2.apps.astra.datastax.com")
            
            if "movie_collection" in db.list_collection_names():
                collection = db.get_collection("movie_collection")
                st.info("Connected to existing collection in Astra DB.")
            else:
                collection = db.create_collection(
                    "movie_collection",
                    service=CollectionVectorServiceOptions(
                        provider="nvidia",
                        model_name="NV-Embed-QA",
                    ),
                )
                st.info("Connected to new collection in Astra DB.")
        except Exception as e:
            st.error(f"Failed to connect to Astra DB: {e}")
            collection = None
    return collection
