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

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    [
        "Australian Market",
        "Suburb Scoring",
        "Suburb / Site Analyzer",
        "AI Property Analysis",
        "Singapore Grants",
        "Grant Matcher",
        "Documents",
        "Roadmap",
    ],
)

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

if page == "Australian Market":
    st.header("Australian Property Market")
    st.dataframe(market_data, use_container_width=True)

elif page == "Suburb Scoring":
    st.header("Suburb Scoring")

    suburb_scores = pd.DataFrame(
        [
            ["Perth", "WA", 91, "High momentum", "Tight supply and strong rental demand"],
            ["Brisbane", "QLD", 88, "Growth", "Population growth and migration"],
            ["Adelaide", "SA", 80, "Stable growth", "Relative affordability"],
            ["Melbourne", "VIC", 79, "Recovery", "Post-cycle recovery potential"],
            ["Sydney", "NSW", 84, "Capital preservation", "Deep long-term demand"],
        ],
        columns=["Market", "State", "Score", "Theme", "Comment"],
    )

    st.dataframe(suburb_scores, use_container_width=True, hide_index=True)

    selected_market = st.selectbox("Select a market", suburb_scores["Market"].tolist())
    row = suburb_scores[suburb_scores["Market"] == selected_market].iloc[0]

    st.subheader(f"{row['Market']} Market Snapshot")
    st.write(f"Score: {row['Score']}")
    st.write(f"Theme: {row['Theme']}")
    st.write(f"Notes: {row['Comment']}")

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

    st.subheader("Sample Opportunity Table")
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

Provide a practical property analysis for:

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

    file = st.file_uploader("Upload report", type=["pdf", "txt", "csv"])

    if file:
        st.success(f"Uploaded {file.name}")

elif page == "Roadmap":
    st.header("Platform Roadmap")

    roadmap = pd.DataFrame(
        {
            "Phase": ["1", "2", "3", "4"],
            "Goal": [
                "Property dashboard",
                "AI analysis",
                "Singapore grants navigator",
                "Document AI",
            ],
        }
    )

    st.dataframe(roadmap, use_container_width=True)
