import streamlit as st
from astradb.db_connection import connect_to_astra
from astradb.vector_search import perform_vector_search
from openai_client import initialize_openai, generate_recommendation

# Initialize the OpenAI client 
OPENAI_API_KEY = "Open API Keys here"
initialize_openai(OPENAI_API_KEY)

def search_movie():
    st.subheader("Search for Movies")
    query = st.text_input("Enter search terms related to the movie:")
    
    if query:
        # Connect to Astra DB and perform vector search
        collection = connect_to_astra()
        results = perform_vector_search(collection, query)
        
        if results:
            for result in results:
                title = result.get('title', 'No Title')
                description = result.get('description', 'No Description')
                poster_url = result.get('poster_url', None)
                similarity = result.get('$similarity', None)
                
                st.subheader(f"{title}" + (f" (Similarity: {similarity:.4f})" if similarity else ""))
                if poster_url:
                    st.image(poster_url, width=300)
                st.write(f"Description: {description}")
                
                # Generate and display the recommendation
                with st.spinner("Generating recommendation..."):
                    explanation = generate_recommendation(query, title, description)
                
                st.markdown(
                    f"<p style='color: #FF5722; font-weight: bold;'>Why Recommended:</p> <p style='color: #4CAF50;'>{explanation}</p>",
                    unsafe_allow_html=True
                )
                
                st.markdown("---")
        else:
            st.write("No movies found matching your search criteria.")

def main():
    st.markdown("""
    <style>
    .title-font {
        font-size: 28px;
        font-weight: bold;
    }
    .powered-font {
        color: red;
        font-size: 20px;
    }
    </style>
    <div>
        <span class="title-font">Movie Search</span><br>
        <span class="powered-font">Powered By Astra DB Vector Search and OpenAI Generative AI</span>
    </div>
    """, unsafe_allow_html=True)

    search_movie()

if __name__ == "__main__":
    main()
