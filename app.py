import streamlit as st
import pandas as pd
import re
from api.api import generate_bulletpoints

st.set_page_config(page_title="ResumeHubs", page_icon="🔮", layout="wide")
st.title("Resume Keywords Search")
st.subheader("Generate resume bullet points based on keywords from job descriptions or resumes.")
conn = st.connection("snowflake")

st.divider()

col1, col2, col3 = st.columns(3)

search = col1.text_input("Enter the keyword you want to search from the job description", placeholder="Python", key='search')
keyword2 = col2.text_input("Enter another keyword you also want to have in your resume bullet point (Optional)", placeholder="analytics", key='search_2')
keyword3 = col3.text_input("Enter another keyword you also want to have in your resume bullet point (Optional)", placeholder="Microsoft Excel", key='search_3')

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()

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
    global search, keyword2, keyword3

    query = f"SELECT * FROM BULLET_POINTS WHERE BULLET_POINT ILIKE '%{search}%'"
    if keyword2:
        query += f" AND BULLET_POINT ILIKE '%{keyword2}%'"
    if keyword3:
        query += f" AND BULLET_POINT ILIKE '%{keyword3}%'"

    df = conn.query(query, ttl=600)
    if df.empty:
        response = f"No bullet points found for the keywords: {search}"
        if keyword2:
            response += f", {keyword2}"
        if keyword3:
            response += f", {keyword3}"
        st.write(response)
    else:
        df = df.drop(columns=["ID"])
        st.session_state.data = df 
        create_table(st.session_state.data, search, keyword2, keyword3)

def generateBulletPoint():
    global search, keyword2, keyword3

    keywords = [search]
    if keyword2:
        keywords.append(keyword2)
    if keyword3:
        keywords.append(keyword3)
    bullet_points = generate_bulletpoints(keywords, st.session_state.data["BULLET_POINT"].tolist() if not st.session_state.data.empty else [])
    st.success(f"There are {st.session_state.num_bullet_points_generated} new bullet points generated successfully! Copy and use them in your resume.")
    df_new = pd.DataFrame(bullet_points, columns=["BULLET_POINT"])

    st.session_state.data = pd.concat([df_new, st.session_state.data], ignore_index=True)

    create_table(st.session_state.data, search, keyword2, keyword3)

submit = st.button("Search", key="search_button", type="primary")
generate = st.button("Generate more 💡", key="generate_button", type="secondary")

if submit:
    if st.session_state.get('previous_search') != (search, keyword2, keyword3):
        st.session_state.data = pd.DataFrame()
        st.session_state.previous_search = (search, keyword2, keyword3)
    searchBulletPoint()

if generate:
    if st.session_state.get('previous_search') != (search, keyword2, keyword3):
        st.session_state.data = pd.DataFrame()
        st.session_state.previous_search = (search, keyword2, keyword3)
    with st.spinner("Generating new bullet points..."):
        generateBulletPoint()