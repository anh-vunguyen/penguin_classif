print('Rerun')
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Penguin Prediction App

This app predicts the **Palmer Penguin** species.
Data obtained form the *palmerpenguins library* in R by Allison Horst
""")

st.sidebar.header('User Input Features')
st.sidebar.markdown("""
[Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/)
""")

# Collects user input featues into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=['csv'])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_feature():
        island = st.sidebar.selectbox('Island', ('Biscoe', 'Dream', 'Torgersen'))
        sex = st.sidebar.selectbox('Sex', ('male', 'female'))
        bill_length_mm = st.sidebar.slider('Bill length (mm)', 32.1, 59.6, 43.9)
        bill_depth_mm = st.sidebar.slider('Bill depth (mm)', 13.1, 21.5, 17.2)
        flipper_length_mm = st.sidebar.slider('Flipper length (mm)', 172.0, 213.0, 201.0)
        body_mass_g = st.sidebar.slider('Body mass (g)', 2700.0, 6300.0, 4207.0)
        data = {'island': island,
                'bill_length_mm': bill_length_mm,
                'bill_depth_mm': bill_depth_mm,
                'flipper_length_mm': flipper_length_mm,
                'body_mass_g': body_mass_g,
                'sex': sex
                }
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_feature()

# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase
penguins_raw = pd.read_csv('penguins_cleaned.csv')
penguins = penguins_raw.drop(columns=['species'])
df = pd.concat([input_df, penguins], axis=0)

# Encoding of ordinal features
encode = ['sex', 'island']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]
df = df[:1] # select only the first row

# Display the user input feature
st.subheader('User Input Features')
if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below)')
    st.write(df)

# Reads in saved classification model
load_clf = pickle.load(open('penguins_clf.pkl', 'rb'))

# Apply model to make prediction
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader('Prediction')
penguins_species = np.array(['Adelie', 'Chinstrap', 'Gentoo'])
st.write(penguins_species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)
