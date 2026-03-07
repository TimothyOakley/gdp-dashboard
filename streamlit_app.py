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
    layout="wide"
)

st.title("🏘️ Property & Grants AI Platform")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Australian Market",
        "Live Suburb Rankings",
        "Suburb Scoring",
        "Suburb / Site Analyzer",
        "AI Property Analysis",
        "Singapore Grants",
        "Grant Matcher",
        "Documents",
        "Roadmap"
    ]
)

market_data = pd.DataFrame(
    [
        ["Sydney", "NSW", "Capital Growth", "Medium", 84],
        ["Melbourne", "VIC", "Recovery", "Medium", 79],
        ["Brisbane", "QLD", "Growth", "Medium", 88],
        ["Perth", "WA", "High Momentum", "High", 91],
        ["Adelaide", "SA", "Stable Growth", "Low", 80]
    ],
    columns=["Market", "State", "Theme", "Risk", "Score"]
)

site_data = pd.DataFrame(
    [
        ["Parramatta", "NSW", "Apartment", "Transit growth"],
        ["Logan", "QLD", "House", "Affordable housing demand"],
        ["Bayswater", "WA", "Townhouse", "Infill development"],
        ["Geelong", "VIC", "House", "Commuter growth"],
        ["Ipswich", "QLD", "House", "Family demand"]
    ],
    columns=["Suburb", "State", "Asset Type", "Opportunity"]
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
        ["SkillsFuture Enterprise Credit", "Workforce transformation"]
    ],
    columns=["Grant", "Purpose"]
)

# More realistic suburb factors
suburb_factors = pd.DataFrame(
    [
        ["Perth", "WA", 9.2, 6.0, 1.4, 8.3, 7.8, 6.2, "Momentum + Yield"],
        ["Brisbane", "QLD", 8.7, 5.1, 1.1, 8.5, 7.4, 6.8, "Growth"],
        ["Adelaide", "SA", 7.2, 4.8, 0.9, 7.3, 7.2, 8.0, "Stable Growth"],
        ["Sydney", "NSW", 5.8, 3.4, 1.8, 6.7, 5.8, 6.6, "Capital Preservation"],
        ["Melbourne", "VIC", 6.1, 4.0, 1.6, 6.5, 6.1, 7.2, "Recovery"],
        ["Gold Coast", "QLD", 7.0, 4.9, 2.4, 7.4, 6.9, 5.5, "Lifestyle + Yield"],
        ["Geelong", "VIC", 6.8, 4.7, 1.3, 6.9, 6.7, 7.0, "Commuter Growth"],
        ["Ipswich", "QLD", 7.9, 5.6, 2.0, 7.5, 7.5, 6.3, "Affordable Growth"],
        ["Parramatta", "NSW", 6.7, 3.8, 2.6, 7.2, 6.0, 6.4, "Urban Renewal"],
        ["Logan", "QLD", 8.0, 5.8, 2.1, 7.8, 7.7, 6.1, "Value + Demand"]
    ],
    columns=[
        "Suburb",
        "State",
        "Price Growth",
        "Yield",
        "Vacancy Risk",
        "Population Growth",
        "Infrastructure",
        "Affordability",
        "Theme"
    ]
)

def get_api_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")

def run_ai(prompt):
    api_key = get_api_key()

    if not api_key:
        return None, "OPENAI_API_KEY not set"

    if OpenAI is None:
        return None, "OpenAI package missing"

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text, None
    except Exception as e:
        return None, str(e)

def score_suburbs(df, growth_w, yield_w, infra_w, pop_w, afford_w, vacancy_penalty_w):
    scored = df.copy()

    scored["Growth Score"] = (scored["Price Growth"] * 10).round(1)
    scored["Yield Score"] = (scored["Yield"] * 10).round(1)
    scored["Risk Score"] = (100 - (scored["Vacancy Risk"] * 10)).round(1)

    scored["Overall Score"] = (
        scored["Price Growth"] * growth_w +
        scored["Yield"] * yield_w +
        scored["Infrastructure"] * infra_w +
        scored["Population Growth"] * pop_w +
        scored["Affordability"] * afford_w -
        scored["Vacancy Risk"] * vacancy_penalty_w
    ) * 10

    scored["Overall Score"] = scored["Overall Score"].round(1)
    return scored.sort_values("Overall Score", ascending=False)

if page == "Australian Market":
    st.header("Australian Property Market")
    st.dataframe(market_data, use_container_width=True)

elif page == "Live Suburb Rankings":
    st.header("Live Suburb Rankings")
    st.write("Weighted suburb rankings using growth, yield, vacancy risk, population, infrastructure, and affordability.")

    c1, c2, c3 = st.columns(3)
    growth_w = c1.slider("Growth weight", 0.0, 3.0, 1.8, 0.1)
    yield_w = c2.slider("Yield weight", 0.0, 3.0, 1.2, 0.1)
    vacancy_penalty_w = c3.slider("Vacancy penalty", 0.0, 3.0, 1.0, 0.1)

    c4, c5, c6 = st.columns(3)
    infra_w = c4.slider("Infrastructure weight", 0.0, 3.0, 1.1, 0.1)
    pop_w = c5.slider("Population weight", 0.0, 3.0, 1.2, 0.1)
    afford_w = c6.slider("Affordability weight", 0.0, 3.0, 0.9, 0.1)

    ranked = score_suburbs(
        suburb_factors,
        growth_w,
        yield_w,
        infra_w,
        pop_w,
        afford_w,
        vacancy_penalty_w
    )

    state_filter = st.selectbox("Filter by state", ["All"] + sorted(ranked["State"].unique().tolist()))
    min_score = st.slider("Minimum overall score", 0, 100, 60)

    filtered = ranked.copy()
    if state_filter != "All":
        filtered = filtered[filtered["State"] == state_filter]

    filtered = filtered[filtered["Overall Score"] >= min_score]

    st.dataframe(
        filtered[
            [
                "Suburb",
                "State",
                "Growth Score",
                "Yield Score",
                "Risk Score",
                "Overall Score",
                "Theme"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    if not filtered.empty:
        top = filtered.iloc[0]
        st.subheader("Top Ranked Opportunity")
        st.write(f"**{top['Suburb']}, {top['State']}**")
        st.write(f"Theme: {top['Theme']}")
        st.write(f"Overall Score: {top['Overall Score']}")

elif page == "Suburb Scoring":
    st.header("Suburb Scoring")

    suburb_scores = score_suburbs(
        suburb_factors,
        1.8, 1.2, 1.1, 1.2, 0.9, 1.0
    )

    st.dataframe(
        suburb_scores[
            ["Suburb", "State", "Growth Score", "Yield Score", "Risk Score", "Overall Score", "Theme"]
        ],
        use_container_width=True,
        hide_index=True
    )

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

    st.subheader("Sample Development Opportunities")
    st.dataframe(site_data, use_container_width=True)

elif page == "AI Property Analysis":
    st.header("AI Property Analysis")

    query = st.text_input("Enter suburb or property question")

    if st.button("Run Analysis"):
        prompt = f"""
You are an Australian property market expert.

Provide a professional investment analysis for:

{query}

Include:
- outlook
- opportunities
- risks
- rental market
- investor recommendation
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
        "What do you need funding for?",
        [
            "Buy software",
            "Custom digital project",
            "Advanced digital integration",
            "Digital advisory",
            "Overseas expansion"
        ]
    )

    if st.button("Match Grants"):
        if need == "Buy software":
            st.write("Recommended: Productivity Solutions Grant (PSG)")
        elif need == "Custom digital project":
            st.write("Recommended: Enterprise Development Grant (EDG)")
        elif need == "Advanced digital integration":
            st.write("Recommended: Advanced Digital Solutions (ADS)")
        elif need == "Digital advisory":
            st.write("Recommended: CTO-as-a-Service")
        elif need == "Overseas expansion":
            st.write("Recommended: Market Readiness Assistance (MRA)")

elif page == "Documents":
    st.header("Documents")

    file = st.file_uploader("Upload report", type=["pdf", "txt", "csv"])

    if file:
        st.success(f"Uploaded {file.name}")

elif page == "Roadmap":
    st.header("Platform Roadmap")

    roadmap = pd.DataFrame(
        {
            "Phase": ["1", "2", "3", "4", "5"],
            "Goal": [
                "Property dashboard",
                "AI suburb analysis",
                "Singapore grants navigator",
                "Document AI",
                "Weighted suburb rankings"
            ]
        }
    )

    st.dataframe(roadmap, use_container_width=True)
