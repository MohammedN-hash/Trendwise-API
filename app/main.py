import streamlit as st
from requests import get

# Define the URL for the FastAPI app
API_URL = "http://localhost:8080"

# Define the Streamlit app
def app():

    # Add a title and description to the app
    st.title("TrendWise")
    st.write("Analyze topic and get trends")

    # Add a text input for the user to enter a query
    query = st.text_input("Enter a query:")

    # Add a button to submit the query
    if st.button("Submit"):
        # Call the FastAPI endpoint with the query as a parameter
        response = get(f"{API_URL}/getAnalysis?query={query}").json()

        # Display the response in Streamlit
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    app()