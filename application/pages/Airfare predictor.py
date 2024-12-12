import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Import relevant data used in the API
routes_mapping = pd.read_csv("./data/routes_mapping.csv", encoding='UTF-8')

# Airport full name mapping
airport_mapping = {
    "SBBE": "Belém/Val de Cans International Airport",
    "SBGR": "São Paulo/Guarulhos International Airport",
    "SBBR": "Brasília International Airport",
    "SBRF": "Recife/Guararapes International Airport",
    "SBRJ": "Rio de Janeiro–Santos Dumont Airport",
    "SBSP": "São Paulo–Congonhas Airport",
    "SBCF": "Belo Horizonte/Confins International Airport",
    "SBCT": "Curitiba/Afonso Pena International Airport",
    "SBCY": "Cuiabá–Marechal Rondon International Airport",
    "SBFL": "Florianópolis–Hercílio Luz International Airport",
    "SBFZ": "Fortaleza–Pinto Martins International Airport",
    "SBGO": "Goiânia–Santa Genoveva Airport",
    "SBMO": "Maceió/Zumbi dos Palmares International Airport",
    "SBPA": "Porto Alegre–Salgado Filho International Airport",
    "SBSV": "Salvador–Deputado Luís Eduardo Magalhães International Airport",
    "SBVT": "Vitória–Eurico de Aguiar Salles Airport",
    "SBNF": "Joinville–Lauro Carneiro de Loyola Airport",
}

# CSS Styling
css = '''
.stApp {
    background: linear-gradient(135deg, hsl(292, 30%, 35%), hsl(292, 30%, 65%));
    color: white;
}

.stApp > header {
    background-color: transparent;
}

.stApp h1, h2 {
    text-align: center;
    color: white;
}

div.stButton > button:first-child {
    border: 1px solid darkgreen;
    border-radius: 6px;
    background-color: green;
    color: white;
}
'''

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Page title (H1 heading)
st.header(":airplane: Flight Price Predictor :airplane:")

# Cache the API response to prevent redundant calls
@st.cache_data
def fetch_predictions(params, headers):
    try:
        response = requests.get(
            'https://skyai-wagon-108938723002.us-central1.run.app/pricing_forecast',
            params=params,
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

# User Inputs
user_input_route = st.selectbox('Select a route between two airports', routes_mapping['key'])
user_input_months = st.selectbox('Select number of months',[1,2,3,4,5,6,7,8],index=3 )

# Extract departure and arrival airport codes
departure_airport_code, arrival_airport_code = user_input_route.split('_')

# Display full airport names
departure_airport_full = airport_mapping.get(departure_airport_code, departure_airport_code)
arrival_airport_full = airport_mapping.get(arrival_airport_code, arrival_airport_code)

st.text(f'You have selected the route: ** {departure_airport_code} → {arrival_airport_code} **')
st.text(f"Route details: **{departure_airport_full} → {arrival_airport_full}**")

# Prepare API parameters
params = {
    'departure_airport': departure_airport_code,
    'arrival_airport': arrival_airport_code,
    'prediction_period': user_input_months  # Default prediction for 3 months
}

headers = {
    'accept': 'application/json'
}

# Fetch predictions
data = fetch_predictions(params, headers)

# Display results
if "error" in data:
    st.error(data["error"])
else:
    predictions = data.get("preds", [])
    if predictions:
        df = pd.DataFrame({"Month": list(range(1, len(predictions) + 1)), "Predicted Price (BRL)": predictions})
        dft = pd.DataFrame([predictions], columns=[f"Month {i+1}" for i in range(len(predictions))])

        st.write("### Price Predictions")

        st.dataframe(dft,hide_index=True)

        # Plotting the predictions
        st.write("### Predicted Price Trend")
        fig = px.line(df, x="Month", y="Predicted Price (BRL)", title="Predicted Prices Over Time",
                      markers=True, labels={"Month": "Month", "Predicted Price (BRL)": "Price (BRL)"})
        st.plotly_chart(fig)
    else:
        st.warning("No predictions available for the selected route.")
