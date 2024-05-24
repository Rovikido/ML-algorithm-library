import streamlit as st

from app.backend.database.db import DB
from app.backend.processer import process_topic

db = DB()
db.create_tables()

new_topic_glb = ''
add_btn = False

def display_left_column(selected_topic):
    st.sidebar.markdown('<h1 style="font-size: xxx-large;margin-bottom: 14%;">Topics</h1>', unsafe_allow_html=True) 

    # Retrieve all topics
    topics = db.get_topics()

    # Display each topic as a styled button
    add_button = st.sidebar.button("[Add New Topic]")

    # Check if "Add New Topic" button is clicked
    global add_btn
    if add_button or add_btn:
        add_btn = True
        # Reset selected topic
        selected_topic = ""
        # Clear content of right column
        st.empty()

        # Display text input for adding new topic
        new_topic = st.text_input("Enter New Topic: ")
        add_summary = st.checkbox("Add Summary", value=False)
        if new_topic:
            add_btn = False
            print(add_summary)
            process_topic(new_topic, db, add_summary=add_summary)
            
            st.write(f"Loading new topic: {new_topic}")
            

    for topic in topics:
        name = topic.topic_name
        if len(name) > 40:
            name = name[:37] + "..."
        if st.sidebar.button(name, key=topic.topic_id):
            selected_topic = name

    return selected_topic


def display_right_column(selected_topic):
    global add_btn
    if add_btn:
        return
    if selected_topic == "":
        st.markdown('<h1 style="font-size: xxx-large;">Sources</h1>', unsafe_allow_html=True) 
        st.write("Select a topic to view its sources.")
        return
    
    t_id = db.get_topic_id_by_name(selected_topic)
    all_topics = db.get_topics()
    current_topic = [t for t in all_topics if t.topic_id == t_id][-1]
    st.markdown(f'<h1 style="font-size: xxx-large;">{current_topic.topic_name}</h1>', unsafe_allow_html=True)
    if current_topic.topic_summary != "None":
        st.markdown(f'{current_topic.topic_summary}')
    st.write("---")
    if t_id:
        sources = db.get_sources_by_topic(t_id)

        for source in sources:
            icon = "🗎" if source.source_type == 'artice' else "🌐"
            st.markdown(f"## [{icon}]: [{source.source_name}]({source.source_url})")
            st.write(source.source_description)
            st.write("---")
    else:
        st.write("No sources found for the selected topic.")

def main():
    st.set_page_config(layout="wide")

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
