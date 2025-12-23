import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error

st.set_page_config("Linear Regression",layout="centered")

def load_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

st.markdown("""<div class="card">
            <h1>Linear Regression</h1>
            <p>Predict <b> Tip amount </b> from <b> Total Bill </b> using Linear Regression...</p>
            </div>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return sns.load_dataset("tips")
df=load_data()

st.markdown('<div class="card"><h2>Dataset</h2>',unsafe_allow_html=True)
st.dataframe(df.head())
st.markdown('</div>',unsafe_allow_html=True)

x,y=df[["total_bill"]],df["tip"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

scaler=StandardScaler()

x_train=scaler.fit_transform(x_train)
x_test=scaler.transform(x_test)

model=LinearRegression()
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

mae=mean_absolute_error(y_test,y_pred)

rsme=np.sqrt(mean_squared_error(y_test,y_pred))

r2=r2_score(y_test,y_pred)

adj_r2=1-(1-r2)*(len(y_test)-1)/(len(y_test)-2)

st.markdown('<div class="card"><h2>Total bill vs tip</h2>',unsafe_allow_html=True)
fig,ax=plt.subplots()
ax.scatter(df["total_bill"],df["tip"],alpha=0.6)
ax.plot(df["total_bill"],model.predict(scaler.transform(df[["total_bill"]])),color="red")
ax.set_xlabel("Total Bill")
ax.set_ylabel("Tip")
st.pyplot(fig)
st.markdown('</div>',unsafe_allow_html=True)



#Performance

st.markdown('<div class="card"><h2>Model Performance</h2>',unsafe_allow_html=True)
c1,c2=st.columns(2)
c1.metric("Mean Absolute Error (MAE)",f"{mae:.2f}")
c2.metric("Root Mean Squared Error (RSME)",f"{rsme:.2f}")
c3,c4=st.columns(2)
c3.metric("R2 Score",f"{r2:.2f}")
c4.metric("Adjusted R2 Score",f"{adj_r2:.2f}")  
st.markdown('</div>',unsafe_allow_html=True)

# m & c 
st.markdown(f"""
            <div class="card">
            <h3>MOdel intercept & Coefficient</h3>
            <p><b> Coefficient (m) :</b> {model.coef_[0]:.4f} </p>
            <p><b> Intercept (c) :</b> {model.intercept_:.4f} </p>
            </div>
            """,unsafe_allow_html=True)

#Prediction
st.markdown('<div class="card"><h2>Predict Tip Amount</h2>',unsafe_allow_html=True)
bill=st.slider("Total Bill Amount $",float(df.total_bill.min()),float(df.total_bill.max()),30.0)
tip=model.predict(scaler.transform([[bill]]))[0]
st.markdown(f"""
            <div class="prediction-box">
             predicted tip amount is <b>${tip:.2f}</b>
            </div>
            """,unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)   