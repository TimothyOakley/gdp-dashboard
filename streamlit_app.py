import os
import streamlit as st
import pandas as pd

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

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

    st.dataframe(macro, use_container_width=True)

    st.header("Top Opportunities")
    st.dataframe(data, use_container_width=True)

elif page == "Opportunity Scanner":
    st.header("Investment Opportunities")

    sector = st.selectbox("Filter by sector", ["All"] + sorted(data["Sector"].unique()))

    if sector != "All":
        filtered = data[data["Sector"] == sector]
    else:
        filtered = data

    st.dataframe(filtered, use_container_width=True)

elif page == "AI Analysis":
    st.header("AI Investment Analysis")
    company = st.text_input("Enter a company or sector to analyse")

    if st.button("Run AI Analysis"):
        if not company:
            st.warning("Please enter a company or sector.")
        else:
            api_key = None

            try:
                api_key = st.secrets["OPENAI_API_KEY"]
            except Exception:
                api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                st.error("OPENAI_API_KEY is not set in Streamlit Secrets.")
            elif OpenAI is None:
                st.error("The openai package is not installed.")
            else:
                try:
                    client = OpenAI(api_key=api_key)

                    prompt = f"""
Provide a short investment analysis for {company}.
Include:
- market outlook
- key risks
- investment potential
Keep it concise and practical.
"""

                    with st.spinner("Generating analysis..."):
                        response = client.responses.create(
                            model="gpt-4.1-mini",
                            input=prompt
                        )

                    st.subheader("AI Analysis Result")
                    st.write(response.output_text)

                except Exception as e:
                    st.error(f"AI request failed: {e}")

elif page == "Documents":
    st.header("Upload research documents")

    file = st.file_uploader("Upload report", type=["pdf", "txt", "csv"])

    if file:
        st.success(f"Uploaded {file.name}")
        st.info("Document analysis can be added next.")

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

    st.dataframe(roadmap, use_container_width=True)
