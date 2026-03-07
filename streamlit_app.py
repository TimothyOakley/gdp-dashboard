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
        "Suburb / Site Analyzer",
        "AI Property Analysis",
        "Singapore Grants",
        "Grant Matcher",
        "Documents",
        "Roadmap",
    ],
)

# -----------------------------
# Sample Australia property data
# -----------------------------
market_data = pd.DataFrame(
    [
        ["Sydney", "NSW", "Capital Growth", "Medium", 84, "Tight supply, strong long-term demand"],
        ["Melbourne", "VIC", "Recovery", "Medium", 79, "Value pockets after slower period"],
        ["Brisbane", "QLD", "Growth", "Medium", 88, "Population growth and demand support"],
        ["Perth", "WA", "High Momentum", "High", 91, "Low supply and strong rental conditions"],
        ["Adelaide", "SA", "Stable Growth", "Low", 80, "Affordable relative to eastern states"],
        ["Gold Coast", "QLD", "Yield + Growth", "High", 77, "Lifestyle demand but volatile"],
    ],
    columns=["Market", "State", "Theme", "Risk", "Score", "Comment"],
)

site_data = pd.DataFrame(
    [
        ["Parramatta", "NSW", "Apartment", "Medium", "Transit-led demand", "Check oversupply risk"],
        ["Logan", "QLD", "House", "Medium", "Affordability", "Watch infrastructure pipeline"],
        ["Bayswater", "WA", "Townhouse", "High", "Infill growth", "Check zoning and build costs"],
        ["Geelong", "VIC", "House", "Low", "Commuter demand", "Monitor local supply"],
        ["Ipswich", "QLD", "House + Land", "Medium", "Family demand", "Review flood overlays"],
    ],
    columns=["Suburb", "State", "Asset Type", "Risk", "Opportunity", "Key Check"],
)

# -----------------------------
# Singapore grants data
# -----------------------------
grants_data = pd.DataFrame(
    [
        [
            "Enterprise Development Grant (EDG)",
            "Custom transformation, innovation, growth projects",
            "SME / established business",
            "Digital transformation, business upgrading, overseas growth",
            "Medium to Large",
        ],
        [
            "Productivity Solutions Grant (PSG)",
            "Pre-approved digital tools and productivity solutions",
            "SME",
            "Software adoption, standard IT systems, productivity tools",
            "Small to Medium",
        ],
        [
            "Advanced Digital Solutions (ADS)",
            "Advanced and integrated digital capabilities",
            "SME / growth business",
            "Advanced digitalisation, deeper integration",
            "Medium",
        ],
        [
            "SMEs Go Digital",
            "Digital adoption support path",
            "SME",
            "Digital roadmap, solution support, capability building",
            "Small to Medium",
        ],
        [
            "CTO-as-a-Service",
            "Digital advisory and planning",
            "SME",
            "Digital planning, assessment, roadmap",
            "Small",
        ],
        [
            "Market Readiness Assistance (MRA)",
            "Overseas expansion support",
            "SME",
            "Market entry, business development, overseas growth",
            "Medium",
        ],
        [
            "Startup SG / Startup SG Equity",
            "Startup and innovation ecosystem support",
            "Startup",
            "Innovation, fundraising, scaling",
            "Varies",
        ],
        [
            "Tech@SG",
            "Talent support for fast-growing tech firms",
            "Tech company",
            "Hiring and scaling talent",
            "Varies",
        ],
        [
            "SkillsFuture Enterprise Credit (SFEC)",
            "Workforce and enterprise transformation support",
            "Eligible employer",
            "Training, workforce transformation, adoption support",
            "Small to Medium",
        ],
    ],
    columns=["Grant", "Best For", "Company Type", "Typical Use Case", "Project Size"],
)

# -----------------------------
# Helpers
# -----------------------------
def get_api_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")


def run_ai(prompt: str):
    api_key = get_api_key()
    if not api_key:
        return None, "OPENAI_API_KEY is not set in Streamlit Secrets."
    if OpenAI is None:
        return None, "The openai package is not installed."

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )
        return response.output_text, None
    except Exception as e:
        return None, f"AI request failed: {e}"


# -----------------------------
# Pages
# -----------------------------
if page == "Australian Market":
    st.header("Australian Real Estate Market Overview")
    st.write("Starter market intelligence dashboard focused on Australian property opportunities.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Tracked Markets", len(market_data))
    c2.metric("Highest Score", market_data["Score"].max())
    c3.metric("Average Score", round(market_data["Score"].mean(), 1))

    st.subheader("Market Snapshot")
    st.dataframe(market_data, use_container_width=True, hide_index=True)

    st.subheader("Quick Notes")
    for _, row in market_data.sort_values("Score", ascending=False).iterrows():
        st.markdown(
            f"**{row['Market']} ({row['State']})** — {row['Theme']} | "
            f"Risk: {row['Risk']} | Score: {row['Score']} | {row['Comment']}"
        )

elif page == "Suburb / Site Analyzer":
    st.header("Suburb / Site Analyzer")

    state_filter = st.selectbox("Filter by state", ["All"] + sorted(site_data["State"].unique().tolist()))
    asset_filter = st.selectbox("Filter by asset type", ["All"] + sorted(site_data["Asset Type"].unique().tolist()))

    filtered = site_data.copy()
    if state_filter != "All":
        filtered = filtered[filtered["State"] == state_filter]
    if asset_filter != "All":
        filtered = filtered[filtered["Asset Type"] == asset_filter]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.subheader("Custom Site Review")
    suburb = st.text_input("Enter suburb")
    state = st.text_input("Enter state")
    asset_type = st.selectbox("Asset type", ["House", "Apartment", "Townhouse", "Mixed Use", "Development Site"])
    notes = st.text_area("Site notes", placeholder="Example: corner block near station, possible duplex, check zoning")

    if st.button("Generate Site Summary"):
        summary = f"""
Suburb: {suburb or 'Not provided'}
State: {state or 'Not provided'}
Asset Type: {asset_type}
Notes: {notes or 'No notes provided'}

Suggested checks:
- demand drivers
- supply risk
- planning / zoning issues
- rental appeal
- development feasibility
"""
        st.code(summary)

elif page == "AI Property Analysis":
    st.header("AI Property Analysis")

    property_focus = st.text_input("Enter market, suburb, asset type, or question")
    strategy = st.selectbox(
        "Analysis type",
        [
            "Market outlook",
            "Buy / hold / avoid",
            "Development site review",
            "Rental yield / cashflow view",
            "Risks and opportunities",
        ],
    )

    user_notes = st.text_area(
        "Optional notes",
        placeholder="Example: Looking at Perth houses near transport corridors with redevelopment potential.",
    )

    if st.button("Run Property AI Analysis"):
        if not property_focus:
            st.warning("Please enter a market, suburb, asset type, or question.")
        else:
            prompt = f"""
You are an Australian real estate analyst.

Provide a practical analysis for:
Focus: {property_focus}
Analysis type: {strategy}
User notes: {user_notes}

Please include:
- market outlook
- major risks
- opportunity drivers
- what to verify next
- a short conclusion

Keep it concise, practical, and commercially useful.
"""
            with st.spinner("Generating property analysis..."):
                result, error = run_ai(prompt)

            if error:
                st.error(error)
            else:
                st.subheader("AI Property Analysis Result")
                st.write(result)

elif page == "Singapore Grants":
    st.header("Singapore IT / Digital / PropTech Grants")
    st.write("Starter reference table for Singapore grants and support schemes relevant to IT, digital, and innovation projects.")

    st.dataframe(grants_data, use_container_width=True, hide_index=True)

    st.subheader("Quick Guidance")
    st.markdown(
        """
- **PSG** → best for standard software and pre-approved productivity tools  
- **EDG** → best for larger custom transformation or innovation projects  
- **ADS** → best for deeper or more advanced digital capability builds  
- **CTO-as-a-Service** → best for planning what to do next  
- **MRA** → best for overseas expansion  
- **Startup SG / Tech@SG** → best for startups and talent support  
"""
    )

elif page == "Grant Matcher":
    st.header("Grant Matcher")

    company_stage = st.selectbox("Company stage", ["Startup", "SME", "Established business", "Fast-growing tech company"])
    project_need = st.selectbox(
        "Main need",
        [
            "Buy standard software",
            "Custom digital transformation",
            "Advanced digital integration",
            "Digital roadmap / advisory",
            "Overseas expansion",
            "Hiring / talent support",
            "Training / workforce transformation",
        ],
    )
    project_size = st.selectbox("Project size", ["Small", "Medium", "Large"])

    if st.button("Match Grants"):
        matches = []

        if project_need == "Buy standard software":
            matches = ["Productivity Solutions Grant (PSG)", "SMEs Go Digital"]
        elif project_need == "Custom digital transformation":
            matches = ["Enterprise Development Grant (EDG)"]
        elif project_need == "Advanced digital integration":
            matches = ["Advanced Digital Solutions (ADS)", "Enterprise Development Grant (EDG)"]
        elif project_need == "Digital roadmap / advisory":
            matches = ["CTO-as-a-Service", "SMEs Go Digital"]
        elif project_need == "Overseas expansion":
            matches = ["Market Readiness Assistance (MRA)", "Enterprise Development Grant (EDG)"]
        elif project_need == "Hiring / talent support":
            matches = ["Tech@SG"]
        elif project_need == "Training / workforce transformation":
            matches = ["SkillsFuture Enterprise Credit (SFEC)"]

        st.subheader("Recommended Matches")
        for m in matches:
            st.markdown(f"- **{m}**")

        st.info(
            f"Profile: {company_stage} | Need: {project_need} | Project size: {project_size}"
        )

    st.subheader("AI Grant Analysis")
    grant_question = st.text_area(
        "Ask a grants question",
        placeholder="Example: Which Singapore grants best fit a proptech SME building a custom AI property platform?",
    )

    if st.button("Run Grant AI Analysis"):
        if not grant_question:
            st.warning("Please enter a grants question.")
        else:
            prompt = f"""
You are a Singapore grants advisor focused on IT, digital, AI, and proptech businesses.

Answer this question:
{grant_question}

Please include:
- most relevant grants or support schemes
- why they fit
- what kind of project they are suited for
- what the business should prepare next

Keep it concise and practical.
"""
            with st.spinner("Generating grants analysis..."):
                result, error = run_ai(prompt)

            if error:
                st.error(error)
            else:
                st.subheader("AI Grant Analysis Result")
                st.write(result)

elif page == "Documents":
    st.header("Documents")
    st.write("Use this page later for property reports, grant documents, or application drafts.")

    uploaded_file = st.file_uploader("Upload file", type=["pdf", "txt", "csv", "docx"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        st.info("Document AI review can be added next.")

elif page == "Roadmap":
    st.header("Roadmap")

    roadmap = pd.DataFrame(
        {
            "Phase": ["1", "2", "3", "4", "5"],
            "Goal": [
                "Australian market dashboard",
                "AI property analysis",
                "Singapore grants navigator",
                "Document intelligence",
                "Planning / data integrations",
            ],
            "Status": ["Done", "Done", "Done", "Next", "Planned"],
        }
    )

    st.dataframe(roadmap, use_container_width=True, hide_index=True)
