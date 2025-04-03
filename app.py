import streamlit as st
import openai

# 1. Mock Data -----------------------------------------------------------------

# Mock VC data
vc_list = [
    {"name": "OpenFound", "focus": "AI/Healthcare"},
    {"name": "Greentech Ventures", "focus": "Climate/Environmental"},
    {"name": "Edunation Fund", "focus": "Education/EdTech"},
    {"name": "FinFlow Capital", "focus": "Fintech/Blockchain"}
]

# Mock challenges (public startup problems)
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

# List to hold user-submitted ideas (we'll store them in memory for demo)
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

# 2. Configure OpenAI (Placeholder) --------------------------------------------
# In a real scenario, you must set your API key:
# openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_ai_ideas(user_prompt):
    """
    Example function to call OpenAI GPT API.
    For demonstration, we mock the response with sample text.
    Replace the mock response with an actual API call.
    """
    # If using real OpenAI calls, you might do:
    #
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful startup idea generator."},
    #         {"role": "user", "content": user_prompt}
    #     ],
    #     max_tokens=200
    # )
    #
    # answer = response["choices"][0]["message"]["content"]
    #
    # For demonstration, we'll return a static string:
    answer = (
        f"**AI-Generated Startup Ideas for '{user_prompt}'**\n\n"
        "- **Idea 1:** Build a decentralized supply chain tracking system with blockchain.\n"
        "- **Idea 2:** Create an AI-driven supplier risk analysis platform.\n"
        "- **Idea 3:** Offer a next-gen logistic route optimization service with real-time data."
    )
    return answer


# 3. Streamlit Layout ----------------------------------------------------------

def main():
    st.set_page_config(page_title="Hatcher MVP", layout="wide")

    # Title and intro
    st.title("Hatcher: Startup Problem + Idea Discovery")
    st.markdown(
        "A platform that **curates real-world startup problems** using AI + trend signals + market data, "
        "matching them to **aspiring founders**, **investors/VCs**, and **operators** who want to collaborate."
    )

    # Sidebar with mock VCs
    st.sidebar.title("🔍 Investor Focus")
    st.sidebar.write("Meet the mock investor groups:")
    for vc in vc_list:
        st.sidebar.markdown(f"- **{vc['name']}**: {vc['focus']}")

    st.sidebar.write("---")
    st.sidebar.title("💼 Submit Your Idea")
    st.sidebar.write("Share your startup idea below:")

    # Idea submission form in sidebar
    with st.sidebar.form("idea_submission_form", clear_on_submit=True):
        new_idea_title = st.text_input("Idea Title")
        new_idea_description = st.text_area("Idea Description")
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
            st.success("Your idea has been submitted!")

    # Tabs for main content
    tab1, tab2, tab3 = st.tabs(["1. AI Idea Generator", "2. Public Challenges", "3. View Submitted Ideas"])

    # 3.1. AI Idea Generator tab -----------------------------------------------
    with tab1:
        st.subheader("Generate Startup Ideas Using AI")
        user_prompt = st.text_input("Describe a market or tech you’re interested in:")
        if st.button("Generate Ideas"):
            if user_prompt.strip():
                # Call the AI idea generator
                ai_response = generate_ai_ideas(user_prompt.strip())
                st.markdown(ai_response)
            else:
                st.warning("Please enter a topic or market to generate ideas.")

    # 3.2. Public Challenges tab -----------------------------------------------
    with tab2:
        st.subheader("Explore Public Startup Challenges")
        st.markdown("These are crowdsourced or curated challenges seeking solutions:")

        for challenge in challenges:
            st.markdown(f"### {challenge['title']}")
            st.write(challenge['description'])
            st.write("---")

    # 3.3. View Submitted Ideas tab --------------------------------------------
    with tab3:
        st.subheader("Community-Submitted Ideas")
        st.markdown("Upvote the ideas you find promising!")

        # Display each idea with a vote button
        for i, idea in enumerate(submitted_ideas):
            st.markdown(f"**Title:** {idea['title']}")
            st.markdown(f"**Description:** {idea['description']}")
            st.markdown(f"**Tags:** {idea['tags'] if idea['tags'] else 'N/A'}")
            st.markdown(f"**Votes:** {idea['votes']}")
            st.markdown(f"**Investor Backed?** {'Yes' if idea['investor_backed'] else 'No'}")

            if st.button(f"Upvote {idea['title']}", key=f"upvote_{i}"):
                submitted_ideas[i]['votes'] += 1
                st.success(f"You upvoted '{idea['title']}'!")
            st.write("---")


if __name__ == "__main__":
    main()
