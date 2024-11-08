import streamlit as st

def perform_vector_search(collection, query):
    """Perform a vector search in Astra DB."""
    if not collection:
        return None
    try:
        results_cursor = collection.find(
            sort={"$vectorize": query},
            limit=5,
            projection={"title": True, "description": True, "poster_url": True},
            include_similarity=True
        )
        return list(results_cursor)
    except Exception as e:
        st.error(f"Vector search failed: {e}")
        return None
