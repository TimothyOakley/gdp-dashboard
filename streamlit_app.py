import os
import streamlit as st
import pandas as pd

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

st.set_page_config(
    page_title="Property & Grants AI Platform",
    page_icon="🏘️",
    layout="wide",
)

st.title("🏘️ Property & Grants AI Platform")



# -----------------------------
# Australian market sample data
# -----------------------------

market_data = pd.DataFrame(
    [
        ["Sydney", "NSW", "Capital Growth", "Medium", 84],
        ["Melbourne", "VIC", "Recovery", "Medium", 79],
        ["Brisbane", "QLD", "Growth", "Medium", 88],
        ["Perth", "WA", "High Momentum", "High", 91],
        ["Adelaide", "SA", "Stable Growth", "Low", 80],
    ],
    columns=["Market", "State", "Theme", "Risk", "Score"],
)

site_data = pd.DataFrame(
    [
        ["Parramatta", "NSW", "Apartment", "Transit growth"],
        ["Logan", "QLD", "House", "Affordable housing demand"],
        ["Bayswater", "WA", "Townhouse", "Infill development"],
        ["Geelong", "VIC", "House", "Commuter growth"],
        ["Ipswich", "QLD", "House", "Family demand"],
    ],
    columns=["Suburb", "State", "Asset Type", "Opportunity"],
)

grants_data = pd.DataFrame(
    [
        ["Enterprise Development Grant (EDG)", "Custom transformation"],
        ["Productivity Solutions Grant (PSG)", "Pre-approved IT solutions"],
        ["Advanced Digital Solutions (ADS)", "Advanced digital capabilities"],
        ["SMEs Go Digital", "Digital adoption"],
        ["CTO-as-a-Service", "Digital advisory"],
        ["Market Readiness Assistance (MRA)", "Overseas expansion"],
        ["Startup SG", "Startup support"],
        ["Tech@SG", "Tech talent support"],
        ["SkillsFuture Enterprise Credit", "Workforce transformation"],
    ],
    columns=["Grant", "Purpose"],
)

# -----------------------------
# OpenAI helper
# -----------------------------

def get_api_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")

def run_ai(prompt):
    api_key = get_api_key()

    if not api_key:
        return None, "OPENAI_API_KEY not set."

    if OpenAI is None:
        return None, "openai package missing."

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text, None

    except Exception as e:
        return None, str(e)

# -----------------------------
# Pages
# -----------------------------

if page == "Australian Market":

    st.header("Australian Property Market")

    st.dataframe(market_data, use_container_width=True)

elif page == "Suburb / Site Analyzer":

    st.header("Suburb Investment Analyzer")

    suburb = st.text_input("Enter suburb")
    state = st.text_input("Enter state")
    property_type = st.selectbox(
        "Property type",
        ["House", "Apartment", "Townhouse", "Development Site"]
    )

    if st.button("Analyze Investment Opportunity"):

        prompt = f"""
You are an Australian property market analyst.

Provide an investment analysis for:

Suburb: {suburb}
State: {state}
Property Type: {property_type}

Include:
- market outlook
- population trends
- supply risks
- rental demand
- development potential
- major risks
- investment summary

Keep the analysis practical and investor focused.
"""

        result, error = run_ai(prompt)

        if error:
            st.error(error)
        else:
            st.write(result)

    st.header("Suburb / Site Analyzer")

    st.dataframe(site_data, use_container_width=True)

elif page == "AI Property Analysis":

    st.header("AI Property Analysis")

    query = st.text_input("Enter suburb, market or property question")

    if st.button("Run Analysis"):

        if not query:
            st.warning("Please enter a query")

        else:

            prompt = f"""
You are an Australian property analyst.

Provide an analysis for:

{query}

Include:
- market outlook
- risks
- opportunities
- what to verify before investing
"""

            result, error = run_ai(prompt)

            if error:
                st.error(error)
            else:
                st.write(result)

elif page == "Singapore Grants":

    st.header("Singapore IT & Digital Grants")

    st.dataframe(grants_data, use_container_width=True)

elif page == "Grant Matcher":

    st.header("Grant Matcher")

    need = st.selectbox(
        "What do you need?",
        [
            "Buy software",
            "Custom digital project",
            "Advanced digital integration",
            "Digital advisory",
            "Overseas expansion",
        ],
    )

    if st.button("Match Grants"):

        if need == "Buy software":
            st.write("Recommended: PSG")

        elif need == "Custom digital project":
            st.write("Recommended: EDG")

        elif need == "Advanced digital integration":
            st.write("Recommended: ADS")

        elif need == "Digital advisory":
            st.write("Recommended: CTO-as-a-Service")

        elif need == "Overseas expansion":
            st.write("Recommended: MRA")

elif page == "Documents":

    st.header("Documents")

    file = st.file_uploader("Upload report", type=["pdf","txt","csv"])

    if file:
        st.success(f"Uploaded {file.name}")

elif page == "Roadmap":

    st.header("Platform Roadmap")

    roadmap = pd.DataFrame(
        {
            "Phase": ["1","2","3","4"],
            "Goal": [
                "Property dashboard",
                "AI analysis",
                "Singapore grants navigator",
                "Document AI",
            ],
        }
    )

    st.dataframe(roadmap)
