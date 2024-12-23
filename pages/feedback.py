import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy.sql import text

from style_helper import apply_custom_style

def fetch_feedback_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query("""
        SELECT
            SUM(Satisfied) AS Satisfied,
            SUM(Unsatisfied) AS Unsatisfied
        FROM user_feedback;
        """, ttl=6)
    return df

# Function to insert feedback into the database
def insert_feedback(username, email, comments, satisfied):
    connection = st.connection('mysql', type='sql')
    
    # Map satisfied input to binary values
    satisfied_val = 1 if satisfied == "Yes" else 0
    unsatisfied_val = 1 if satisfied == "No" else 0

    # Default username to "Nobody" if empty
    username = username if username else "Nobody"

    # Use session for transaction management
    with connection.session as session:
        insert_query = text("""
        INSERT INTO user_feedback (UserName, Email, Comments, Satisfied, Unsatisfied)
        VALUES (:username, :email, :comments, :satisfied_val, :unsatisfied_val)
        """)
        
        # Execute the query with parameters using session
        session.execute(insert_query, {
            "username": username,
            "email": email,
            "comments": comments,
            "satisfied_val": satisfied_val,
            "unsatisfied_val": unsatisfied_val
        })
        session.commit()

def main():
    apply_custom_style()

    st.header("User Feedback")

    df = fetch_feedback_data()
    satisfied_count = df['Satisfied'][0]
    unsatisfied_count = df['Unsatisfied'][0]
    
    # Prepare data for pie chart
    feedback_data = pd.DataFrame({
        "Feedback": ["Satisfied", "Unsatisfied"],
        "Count": [satisfied_count, unsatisfied_count]
    })

    # Plot pie chart
    fig = px.pie(
        feedback_data,
        names="Feedback",
        values="Count",
        color="Feedback",
        color_discrete_map={"Satisfied": "#0778DF", "Unsatisfied": "#FF3583"}
    )
    fig.update_traces(textinfo='percent+label')
    
    st.plotly_chart(fig)

    # Entry form for new feedback
    st.header("Submit New Feedback")
    with st.form(key="feedback_form"):
        username = st.text_input("Name (optional)", value="", help="Enter your name.")
        email = st.text_input("Email (required)", value="", help="Please enter your email address.")
        satisfied = st.radio("Are you satisfied (required)?", options=["", "Yes", "No"], index=0, help="Select 'Yes' for satisfied or 'No' for unsatisfied.")
        comments = st.text_area("Comments (optional)", help="Enter any additional comments.")
        
        # Submit button
        submit_button = st.form_submit_button("Submit")
    
        # Insert feedback if form is submitted and email is provided
        if submit_button:
            if not email:
                st.error("Email is required. Please enter your email address.")
            elif not satisfied:
                st.error("Please select 'Yes' or 'No' to indicate if you are satisfied.")
            else:
                insert_feedback(username, email, comments, satisfied)
                st.success("Thank you for your feedback!")
                st.balloons()

if __name__ == "__main__":
    main()
