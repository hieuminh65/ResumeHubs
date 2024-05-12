import streamlit as st
import pandas as pd
import re
from api.api import generate_bulletpoints

st.set_page_config(page_title="ResumeHubs", page_icon="🐍", layout="wide")
st.title("Resume Keywords Search")
st.subheader("Generate resume bullet points based on keywords from job descriptions or resumes.")
conn = st.connection("snowflake")

st.divider()

# Create three columns
col1, col2, col3 = st.columns(3)

# Put each text input field in a separate column
search = col1.text_input("Enter the keyword you want to search from the job description", placeholder="Python", key='search')

keyword2 = col2.text_input("Enter another keyword you also want to have in your resume bullet point (Optional)", placeholder="analytics", key='search_2')

keyword3 = col3.text_input("Enter another keyword you also want to have in your resume bullet point (Optional)", placeholder="Microsoft Excel", key='search_3')

def searchBulletPoint():
    global search
    query = f"SELECT * FROM BULLET_POINTS WHERE BULLET_POINT ILIKE '%{search}%';"
    df = conn.query(query, ttl=600)
    df.drop(df.index[0], inplace=True)
    df = df.drop(columns=["ID"])

    headers = " | ".join(df.columns)
    table = f"| {headers} |\n| {'---|' * len(df.columns)}\n"

    def replace_with_bold(match):
        return f'**{match.group(0)}**'

    for idx, row in df.iterrows():
        row = row.apply(lambda x: re.sub(f'(?i){search}', replace_with_bold, str(x)) if pd.notnull(x) else "")
        table += "| " + " | ".join(row) + " |\n"


    st.markdown(table)

def generateBulletPoint():
    global search
    global keyword2
    global keyword3
    bullet_points = generate_bulletpoints(search)
    bullet_points = "\n".join(bullet_points)
    st.write(bullet_points)

submit = st.button("Search", key="search_button", type="primary")
generate = st.button("Generate more 💡", key="generate_button", type="secondary")


if submit:
    searchBulletPoint()