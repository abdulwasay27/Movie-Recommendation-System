import streamlit as st

def main():
      st.set_page_config(page_title="Cinema Fusion", page_icon="🎥")
      st.title("Welcome to Cinema Fusion🌟")
    
      st.header("About Cinema Fusion")
      st.markdown("""
    **Cinema Fusion** is your go-to movie recommendation system that leverages machine learning to provide personalized movie suggestions. 

    **Key Features:**
    - **Movie Recommendations:** Get tailored movie suggestions based on your preferences.
    - **Sentiment Analysis:** Analyze movie reviews to gauge overall sentiment.
    - **Easy Navigation:** Simple and intuitive interface to help you find and explore movies.

    **How It Works:**
    1. Navigate to the **Search Menu** using the sidebar.
    2. Enter a movie title in the search box.
    3. Explore recommendations based on the movie.
    4. Review sentiment analysis of movie reviews.

    Enjoy your cinematic journey with **Cinema Fusion**!
    """)
if __name__ == "__main__":
    main()
