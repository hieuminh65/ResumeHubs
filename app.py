import streamlit as st
import pandas as pd
import re
from api.api import generate_bulletpoints

st.set_page_config(page_title="ResumeHubs", page_icon="🐍", layout="wide")
st.title("Resume Keywords Search")
st.subheader("Generate resume bullet points based on keywords from job descriptions or resumes.")
conn = st.connection("snowflake")

st.divider()

col1, col2, col3 = st.columns(3)

search = col1.text_input("Enter the keyword you want to search from the job description", placeholder="Python", key='search')

keyword2 = col2.text_input("Enter another keyword you also want to have in your resume bullet point (Optional)", placeholder="analytics", key='search_2')

keyword3 = col3.text_input("Enter another keyword you also want to have in your resume bullet point (Optional)", placeholder="Microsoft Excel", key='search_3')

def create_table(df, search, keyword2=None, keyword3=None):
    headers = " | ".join(df.columns)
    table = f"| {headers} |\n| {'---|' * len(df.columns)}\n"

    def replace_with_bold(match):
        if '**' in match.group(0):
            return match.group(0) 
        return f'**{match.group(0)}**'

    def process_row(x, keyword):
        if pd.notnull(x):
            pattern = rf'\b(?<!\*\*)({keyword})(?!\*\*)\b'
            return re.sub(pattern, replace_with_bold, x, flags=re.IGNORECASE)
        return ""

    for idx, row in df.iterrows():
        row = row.apply(lambda x: process_row(x, search))
        if keyword2:
            row = row.apply(lambda x: process_row(x, keyword2))
        if keyword3:
            row = row.apply(lambda x: process_row(x, keyword3))

        table += "| " + " | ".join(row) + " |\n"

    st.markdown(table, unsafe_allow_html=True)
    return table

def searchBulletPoint():
    query = f"SELECT * FROM BULLET_POINTS WHERE BULLET_POINT ILIKE '% {search} %'"
    if keyword2:
        query += f" AND BULLET_POINT ILIKE '% {keyword2} %'"
    if keyword3:
        query += f" AND BULLET_POINT ILIKE '% {keyword3} %'"
    df = conn.query(query, ttl=600)
    if df.empty:
        if not keyword2 and not keyword3:
            response = f"No bullet points found for the keyword: {search}"
        else:
            response = f"No bullet points found for the keywords: {search}"
            if keyword2:
                response += f", {keyword2}"
            if keyword3:
                response += f", {keyword3}"
        st.write(response)
    else:
        df.drop(df.index[0], inplace=True)
        df = df.drop(columns=["ID"])
        create_table(df, search, keyword2, keyword3)

def generateBulletPoint():
    global search
    global keyword2
    global keyword3
    search = [search]
    if keyword2:
        search.append(keyword2)
    if keyword3:
        search.append(keyword3)
    bullet_points = generate_bulletpoints(search)
    df = pd.DataFrame(bullet_points, columns=["BULLET_POINT"])
    create_table(df, search[0], search[1] if len(search) > 1 else None, search[2] if len(search) > 2 else None)

submit = st.button("Search", key="search_button", type="primary")
generate = st.button("Generate more 💡", key="generate_button", type="secondary")


if submit:
    searchBulletPoint()

if generate:
    generateBulletPoint()