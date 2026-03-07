import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Investment Research Platform", page_icon="📈", layout="wide")

st.title("AI Investment Research Platform")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Opportunity Scanner", "AI Analysis", "Documents", "Roadmap"],
)

data = pd.DataFrame(
    [
        ["BHP", "Mining", "Medium", 82],
        ["CSL", "Healthcare", "Medium", 88],
        ["CBA", "Banking", "Low", 76],
        ["Fortescue", "Mining", "High", 79],
        ["WiseTech", "Technology", "High", 84],
    ],
    columns=["Company", "Sector", "Risk", "Score"],
)

if page == "Dashboard":
    st.header("Market Overview")
    st.write("Example macro indicators")

    macro = pd.DataFrame({
        "Indicator": ["GDP Growth", "Inflation", "Interest Rate"],
        "Value": [2.1, 3.8, 4.35]
    })

    st.dataframe(macro)

    st.header("Top Opportunities")
    st.dataframe(data)

elif page == "Opportunity Scanner":
    st.header("Investment Opportunities")

    sector = st.selectbox("Filter by sector", ["All"] + sorted(data["Sector"].unique()))

    if sector != "All":
        filtered = data[data["Sector"] == sector]
    else:
        filtered = data

    st.dataframe(filtered)

elif page == "AI Analysis":
    st.header("AI Investment Analysis")

    question = st.text_area("Ask an investment question")

    if st.button("Generate analysis"):
        if question:
            st.write("Example AI answer:")
            st.write(
                "Mining stocks may benefit from global infrastructure demand, "
                "while healthcare tends to offer more defensive growth characteristics."
            )

elif page == "Documents":
    st.header("Upload research documents")

    file = st.file_uploader("Upload report", type=["pdf", "txt", "csv"])

    if file:
        st.success(f"Uploaded {file.name}")

elif page == "Roadmap":
    st.header("Platform Roadmap")

    roadmap = pd.DataFrame({
        "Phase": ["1", "2", "3", "4"],
        "Goal": [
            "Working dashboard",
            "AI integration",
            "Document search",
            "Multi-AI model routing"
        ]
    })

    st.dataframe(roadmap)

if page == "AI Analysis":

    st.header("AI Investment Analysis")

    company = st.text_input("Enter a company or sector to analyse")

    if st.button("Run AI Analysis"):

        client = OpenAI()

        prompt = f"""
        Provide a short investment analysis for {company}.
        Include:
        - market outlook
        - key risks
        - investment potential
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        st.write(response.output_text)