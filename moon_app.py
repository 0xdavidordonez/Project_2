import streamlit as st
import plotly.express as px
import altair as alt
import numpy as np
from openai import OpenAI


#STEAMLIT Page layout configuration
st.set_page_config(page_title="To The Moon!!", page_icon=":rocket:", layout="wide")

#title
st.title(" :full_moon: :crystal_ball: Lunar Cycles Trading Strategy :magic_wand: :new_moon:")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

# Introduction Statement
st.markdown("# Bitcoin trading strategy based on lunar cycles")



st.markdown("""
## Welcome to the Moon App :rocket:!

Are you ready to explore the fascinating realm where lunar cycles intersect with the world of trading? Welcome aboard the Moon App, where we delve into the intriguing connection between the phases of the moon and Bitcoin trading. Our mission is to develop an easy trading strategy leveraging signals from Bollinger Bands and lunar cycles, specifically focusing on the full moon and new moon phases. 

## What is it?

The Moon App is an innovative project designed to harness the power of celestial events in guiding Bitcoin trading decisions. By integrating signals from Bollinger Bands with the lunar cycle, particularly during full moon and new moon phases, we aim to develop a unique trading strategy that capitalizes on the potential correlations between lunar cycles and market behavior. With our platform, traders can explore a novel approach to analyzing market trends, gaining insights into how lunar phases may impact asset prices and trading dynamics.

A 20-year study by the University of Lausanne showed that trading strategies based on the full moon and lunar cycles outperformed the overall market by an average of 3.3% per year.
Also, according to a study conducted by the University of Zurich, trading strategies based on the lunar cycle have outperformed the market by an average of 6.8% per year over a period of five years.

## Objective

Our primary objective with the Moon App is to provide traders with a sophisticated yet accessible tool for incorporating lunar cycle analysis into their trading strategies. By executing buy signals when the asset touches the lower Bollinger Band during a full moon and sell signals when it touches the upper band during a new moon, we aim to empower traders to make informed decisions based on both technical indicators and lunar phenomena. Through this integration, we strive to enhance trading performance and unlock new avenues for profitability in the dynamic world of Bitcoin trading.



""")

st.markdown("## Our strategies")

st.markdown("""
We created two trading strategies, one using Bollinger bands, and another using Moon phases...

st.markdown("### Bitcoin + Bollinger Bands")

# 1. Generate Signals (Vectorized and Faster)
btc_df['Signal'] = 0.0

# Buy (1.0) when Close is below Lower Band
btc_df.loc[btc_df['Close'] < btc_df['BB_LOWER'], 'Signal'] = 1.0

# Sell (-1.0) when Close is above Upper Band
btc_df.loc[btc_df['Close'] > btc_df['BB_UPPER'], 'Signal'] = -1.0

# 2. Shift the Signal (THE FIX for Look-Ahead Bias)
# We shift by 1 to use today's signal to trade tomorrow's return.
btc_df['Position'] = btc_df['Signal'].shift(1)

# 3. Calculate Returns
btc_df['Actual_Returns'] = btc_df['Close'].pct_change()

# Use 'Position' (the shifted Signal) to calculate strategy returns
btc_df['Strategy_Returns'] = btc_df['Actual_Returns'] * btc_df['Position']

# 4. Calculate Cumulative Returns
plot_df = btc_df.dropna()
plot_df['Cumulative_Actual_Returns'] = (1 + plot_df['Actual_Returns']).cumprod()
plot_df['Cumulative_Strategy_Returns'] = (1 + plot_df['Strategy_Returns']).cumprod()

# 5. Plot the Chart
st.write("### Corrected Strategy Performance")
st.line_chart(plot_df[['Cumulative_Actual_Returns', 'Cumulative_Strategy_Returns']])

st.markdown("## The Machine learning model")

st.markdown("## The Machine learning model")

st.markdown("""
We used the Logistic Regression model to create predictions for the Moon Phase Strategy.
""")

st.markdown("""
### Classification Report
| | precision | recall | f1-score | support |
|---|---|---|---|---|
| **-1.0** | 1.00 | 0.45 | 0.62 |
| **1.0** | 0.66 | 1.00 | 0.79 |
| **accuracy** | 0.73 | 0.73 | 0.73 |
| **macro avg** | 0.83 | 0.72 | 0.70 |
| **weighted avg** | 0.82 | 0.73 | 0.71 |
""")







st.markdown("<h2 style='color:lightBlue'> Bitcoin + Moon Phases</h3>", unsafe_allow_html=True)
st.markdown(""" the signals:

signals = []

for date, row in merged_df.iterrows():
    
    if row['Moon Phase'] == 'Full Moon':
        
        signals.append(1)  
    
    elif row['Moon Phase'] == 'New Moon':
        
        signals.append(-1)  
    
    else:
        
        signals.append(0)  


""")

st.image('./btc_moon_scattered.png')
st.image('./moon+signals.png')
st.image('./cum_returns_plot_moon.png')

st.markdown("""## The Machine learning model and report""")
st.markdown(""" We used SMOTE technique to deal with the inbalanced data, in order to oversample the minority classes, paired with BalancedRandomForestClassifier.
""")

st.markdown("""New classification report:
|           | precision | recall | f1-score | support |
|-----------|-----------|--------|----------|---------|
| -1        | 0.06      | 0.25   | 0.09     | 28      |
| 0         | 0.94      | 0.67   | 0.79     | 745     |
| 1         | 0.05      | 0.30   | 0.09     | 27      |
| **accuracy** |           |        | 0.65     | 800     |
| **macro avg**| 0.35      | 0.41   | 0.32     | 800     |
| **weighted avg**| 0.88   | 0.65   | 0.74     | 800     |

**Summary:**  
The accuracy of the classifier is 0.65, indicating that it correctly predicts the class label for 65% of the samples. The weighted average F1-score is 0.74, showing that the model performs reasonably well in terms of precision and recall across all classes, with a slight skew towards class 0.
""")

st.markdown("<h2 style='color:Green'>Bollinger Bands + Lunar Phase signals </h3>", unsafe_allow_html=True)

st.markdown(""" the signals:

Signals = []

for index, row in trade_signals_df.iterrows():
    
    if row['Moon Phase'] == 'New Moon' or row['Close'] <= row['BB_LOWER']:
        
        Signals.append(1)  
    
    elif row['Moon Phase'] == 'Full Moon' or row['Close'] >= row['BB_UPPER']:
        
        Signals.append(-1)  
    
    elif row['Moon Phase'] == 'New Moon' or row['Low'] < row['BB_MIDDLE']:
        
        Signals.append(1)  
    
    else:
        
        Signals.append(0)  


""")

st.image('./btc_bb+moon_signals.png')


st.title('MoonGPT :crystal_ball:')
st.caption('A finance guru bot with infinite knowledge about finance.')

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me questions about finance"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})