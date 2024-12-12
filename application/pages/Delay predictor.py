# Streamlit user interface
import streamlit as st
import requests
import pandas as pd

# CSS styyling snippets to change the background, header styling, and
# submit button
css = '''
.stApp {
    background: #9E59AA;
}

.stApp > header {
    background-color: transparent;
}

.stApp > h1, h2 {
    text-align: center;
    font-size: 3em;
}

div.stButton > button:first-child {
    border: 1px solid darkgreen;
    border-radius: 6px;
    background-color: green;
}

'''

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# Page title (H1 heading)
st.header(":airplane: Flight Delay Predictor :clock4:")

df_flight = pd.read_csv("../data/flight-detail-grouped.csv")
df_flight.drop(columns='Unnamed: 0')

with st.form(key='params_for_api'):

    user_input_flight_number= st.selectbox("Select a flight", df_flight['flight.number'])
    user_input_month = st.selectbox("Select month",[1,2,3,4,5,6,7,8,9,10,11,12])
    # flight_number = st.number_input('Flight number')
    # departure_month = st.number_input('Month of departure')
    st.form_submit_button('Check for delay')

    params = {
        'flight_number': user_input_flight_number,
        'departure_month': user_input_month
    }
    # params = dict(
    #     flight_number = flight_number,
    #     departure_month = departure_month
    # )

user_output_base_str1 = "Your flight will most likely "
user_output_base_str2 = "be delayed. Probability: "
# true_false_str = ""

headers = {
    'accept': 'application/json'
}

flight_delay_api_url = 'https://skyai-wagon-108938723002.us-central1.run.app/delay_proba'

response = requests.get(flight_delay_api_url, params=params, headers=headers)

# Carry out response handling if successful call to API
if response.status_code == 200:
    prediction = response.json()
    pred_true = prediction['outcome']
    pred_prob = prediction['proba_delay']

    # If a delay is likely, set the output string accordingly & display
    true_false_str = "" if pred_true == "Delayed" else "not "

    # Display output as a header title
    st.subheader(user_output_base_str1 + true_false_str + user_output_base_str2\
               + f"{pred_prob:.0%}")
