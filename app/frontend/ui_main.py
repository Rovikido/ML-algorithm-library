import streamlit as st

from app.backend.database.db import DB
from app.backend.processer import process_topic

db = DB()
db.create_tables()

def display_left_column(selected_topic):
    st.sidebar.markdown('<h1 style="font-size: xxx-large;margin-bottom: 14%;">Topics</h1>', unsafe_allow_html=True) 

    # Retrieve all topics
    topics = db.get_topics()

    # Display each topic as a styled button
    # st.sidebar.markdown("---")
    for topic in topics:
        # st.sidebar.markdown('<div style="margin-bottom: 5%;"></div>', unsafe_allow_html=True)
        name = topic.topic_name
        if len(name)>40:
            name = name[:17] + "..."
        if st.sidebar.button(name, key=topic.topic_id):
            selected_topic = name
        
        # Add a separator between topics
        # st.sidebar.markdown("---")

    return selected_topic

def display_right_column(selected_topic):
    st.markdown('<h1 style="font-size: xxx-large;">Sources</h1>', unsafe_allow_html=True) 
    if selected_topic == "":
        st.write("Select a topic to view it\'s sources.")
        return
    # Retrieve sources for the selected topic
    t_id = db.get_topic_id_by_name(selected_topic)
    if t_id:
        sources = db.get_sources_by_topic(t_id)

        for source in sources:
            st.markdown(f"## [{source.source_name}]({source.source_url})")  # Display as hyperlink
            st.write(source.source_description)
            st.write("---")  # Add a separator between sources
    else:
        st.write("No sources found for the selected topic.")

def main():
    st.set_page_config(layout="wide")

    # Display left and right columns
    selected_topic = display_left_column("")
    display_right_column(selected_topic)
    st.markdown("""
    <style>
    /* CSS selector to target Streamlit button */
    div[data-testid="stButton"] > button {
        /* Your custom styles */
        background-color: #f0f0f0;
        color: black; /* Text color */
        text-align: left; /* Text alignment */
        width: 100%; /* Width */
        font-size: xx-large;
        border-top: 1px solid gray; /* Top border */
        border-bottom: none; /* Bottom border */
        border-left: none; /* Remove left border */
        border-right: none; /* Remove right border */
        border-radius: 0px; /* Border radius */
        cursor: pointer; /* Cursor */
        margin: -10px 0 -10px 0;
        padding: 0;
    }


    /* CSS selector to target Streamlit button hover state */
    div[data-testid="stButton"] > button:hover {
        background-color: #e0e0e0; /* Change background color on hover */
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
