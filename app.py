import streamlit as st
import openai

# --- 1. Mock Data ----------------------------------------------------------------

# Mock VC data
vc_list = [
    {"name": "OpenFound", "focus": "AI/Healthcare"},
    {"name": "Greentech Ventures", "focus": "Climate/Environmental"},
    {"name": "Edunation Fund", "focus": "Education/EdTech"},
    {"name": "FinFlow Capital", "focus": "Fintech/Blockchain"}
]

# Mock challenges (example “VC-curated” public startup problems)
challenges = [
    {
        "title": "AI-Powered Healthcare Diagnosis",
        "description": (
            "Build an AI tool to assist doctors in diagnosing diseases faster "
            "and more accurately. The tool should leverage patient data, "
            "medical literature, and real-time imaging to suggest probable diagnoses."
        )
    },
    {
        "title": "Sustainable Packaging for E-Commerce",
        "description": (
            "Develop eco-friendly packaging solutions that reduce plastic waste "
            "and lower shipping costs. Consider renewable materials and innovative "
            "product design."
        )
    },
    {
        "title": "Gamified Education for Underserved Regions",
        "description": (
            "Create an accessible, gamified education platform for students "
            "in areas with limited internet access. Consider offline functionality "
            "and localized content."
        )
    }
]

# Mock user-submitted solutions/ideas (in-memory only for demo)
submitted_ideas = [
    {
        "title": "Instant Doc AI",
        "description": "An AI that uses patient symptom checkers and imaging for quick triage.",
        "votes": 10,
        "investor_backed": False,
        "tags": ["healthcare", "AI"]
    },
    {
        "title": "Plant-based Biodegradable Foam",
        "description": "Eco-foam for e-commerce packaging that decomposes within weeks.",
        "votes": 7,
        "investor_backed": True,
        "tags": ["climate", "packaging"]
    }
]

# --- 2. Configure OpenAI ----------------------------------------------------------
# In real production usage, store the key in secrets or env variables, not hard-coded.
openai.api_key = "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"  # <--- Replace with your actual key or st.secrets["OPENAI_API_KEY"]

def generate_ai_ideas(user_prompt: str) -> str:
    """
    Sends the user prompt to GPT (e.g. gpt-3.5-turbo) to get a list of potential 
    real-world problems in that domain. This is a simplified example.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI that researches startup problems by analyzing hundreds "
                        "of articles and news. Provide validated or emerging problems in the given domain. "
                        "Make them specific, with a sense of urgency or impact."
                    )
                },
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        # Fallback or error
        return f"Error generating problems: {e}"

# --- 3. Streamlit Layout ----------------------------------------------------------
def main():
    st.set_page_config(page_title="Hatcher MVP", layout="wide")

    # Title and intro
    st.title("Hatcher: Startup Problem + Idea Discovery")
    st.markdown(
        """
        **Hatcher** is a platform that combines **AI research**, **VC insights**, and **community collaboration** to:
        - Uncover **unique, validated problems** for aspiring founders
        - Allow **VCs** to propose or scout problems and solutions
        - Match solutions and ideas with potential investors
        - Provide a **public forum** where founders can post solutions anonymously and VCs can pledge interest
        """
    )

    st.write("---")

    # --- Sidebar with mock VCs ---
    st.sidebar.title("🔍 Investor Focus")
    st.sidebar.write("Meet our example investor groups:")
    for vc in vc_list:
        st.sidebar.markdown(f"- **{vc['name']}**: {vc['focus']}")

    st.sidebar.write("---")
    st.sidebar.title("💼 Submit Your Solution")
    st.sidebar.write("Already have a startup idea or solution to a problem? Share it here!")

    # Sidebar form: Submit a new idea
    with st.sidebar.form("idea_submission_form", clear_on_submit=True):
        new_idea_title = st.text_input("Solution/Idea Title")
        new_idea_description = st.text_area("Describe your solution")
        new_idea_tags = st.text_input("Tags (comma-separated)")
        submit_idea_button = st.form_submit_button("Submit Idea")

        if submit_idea_button and new_idea_title and new_idea_description:
            submitted_ideas.append({
                "title": new_idea_title,
                "description": new_idea_description,
                "votes": 0,
                "investor_backed": False,
                "tags": [tag.strip() for tag in new_idea_tags.split(",") if tag.strip()]
            })
            st.success("Your solution/idea has been submitted!")

    # --- TABS: (1) AI Problem Finder, (2) Public Challenges, (3) View Submissions ---
    tab1, tab2, tab3 = st.tabs([
        "1. AI Problem Finder",
        "2. Public Challenges",
        "3. View Submitted Solutions"
    ])

    # --- Tab 1: AI Problem Finder ---
    with tab1:
        st.subheader("Discover a Real-World Problem")
        st.markdown(
            "Need a **unique problem** for your next startup? Let our AI scour "
            "articles, news, and trends to propose **pressing, emerging** challenges."
        )

        user_prompt = st.text_input(
            "Enter a market/tech domain (e.g. 'fintech for the unbanked', 'edge AI in healthcare')",
            key="problem_prompt_input"
        )
        if st.button("Find Problems", key="problem_finder_button"):
            if user_prompt.strip():
                with st.spinner("AI is researching..."):
                    response = generate_ai_ideas(user_prompt.strip())
                    st.markdown("### Potential Problems to Solve")
                    st.write(response)
            else:
                st.warning("Please enter a domain or market to find problems.")

    # --- Tab 2: Public Challenges ---
    with tab2:
        st.subheader("VC-Curated Public Challenges")
        st.markdown(
            "Here are **problems** curated or posted by our partner VCs. "
            "Founders can propose solutions anonymously or openly."
        )

        for challenge in challenges:
            st.markdown(f"### {challenge['title']}")
            st.write(challenge['description'])
            st.write("---")

    # --- Tab 3: View Submitted Solutions (with voting) ---
    with tab3:
        st.subheader("Community-Submitted Solutions")
        st.markdown("Upvote the solutions you find promising! VCs can see top-voted ideas.")

        for i, idea in enumerate(submitted_ideas):
            st.markdown(f"**Title:** {idea['title']}")
            st.markdown(f"**Description:** {idea['description']}")
            st.markdown(f"**Tags:** {', '.join(idea['tags']) if idea['tags'] else 'N/A'}")
            st.markdown(f"**Votes:** {idea['votes']}")
            st.markdown(f"**Investor Backed?** {'Yes' if idea['investor_backed'] else 'No'}")

            if st.button(f"Upvote '{idea['title']}'", key=f"upvote_{i}"):
                submitted_ideas[i]['votes'] += 1
                st.success(f"You upvoted '{idea['title']}'!")
            st.write("---")


if __name__ == "__main__":
    main()
