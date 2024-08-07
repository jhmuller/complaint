import os
import datetime
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import openai

openai.api_key = load_dotenv(find_dotenv())
client = OpenAI()
st.markdown("""
  <style>
      span[data-baseweb="tag"][role="button"]{
          background-color: blue;
      }
  </style>

  """, unsafe_allow_html=True)

problems = st.multiselect("Choose your issues",
                        ("lost luggage", "delayed flight", "cancelled flight"))
issues = ", and".join(problems)


results = st.multiselect("Choose your issues",
                        ("missed event", "missed connection", ))
consequences = ", and".join(results)

tone = st.selectbox(
    "what tone would you like to use in the letter?",
    ("polite", "polite but firm", "annoyed", "livid")
)
airline   = st.selectbox(
    "which airline?",
    ("Delta", "American", "SouthWest", "United"))
compensation = st.selectbox("What kind of compensation do you want?",
                            ("cash", "free flight", "reward miles"))


def write_letter(airline="delta",
                 issues="missed flight",
                 consequences="missed event",
                 tone="annoyed",
                 compensation="cash"):
    if compensation and tone and airline and issues and consequences:
        user_request =  f"""My name is John Smith and today's date is {datetime.date.today().strftime('%B %d, %Y')}
        On August 3 I was scheduled to fly from Montreal to Atlanta on {airline}.
            Unfortunately I had the following issues: {issues}.
            which caused  further issues: {consequences}.

            I need a letter to send to the airline, written in a {tone} tone
             to express my dissatisfaction.
            In the letter I want to ask for {compensation} as compensation.

            My name is John Smith and my address is 1 Main St., Anywhere, NC.
            My email is john.smith$gmail.com
        Please generate the letter"""
        #st.write (user_request)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful letter writing assistant."},
                {"role": "user", "content": user_request }]
        )
    st.text_area("Generated Letter",response.choices[0].message.content, height=400)
    return response
# airline = "Delta"
# tone = "livid"
# issues = ", and".join(["delayed flight", "lost luggage"])
# consequences = "missed event"
# compensation = "cash"
# response = write_letter(airline=airline,
#              issues=issues,
#              consequences=consequences,
#              tone=tone,
#              compensation=compensation
#                          )
but = st.button("Write Letter", on_click=write_letter,
                kwargs={"airline":airline,
                        "issues": issues,
                        "consequences": consequences,
                        "tone": tone,
                        "compensation": compensation})
