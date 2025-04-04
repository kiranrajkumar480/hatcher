import streamlit as st
import requests

# --------------------------------------------------------------------------------
# 1. Groq API Setup (Hard-coded for DEMO — in production, store in st.secrets!)
# --------------------------------------------------------------------------------
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --------------------------------------------------------------------------------
# 2. Mock Data
# --------------------------------------------------------------------------------
vc_list = [
    {"name": "OpenFound", "focus": "AI/Healthcare"},
    {"name": "Greentech Ventures", "focus": "Climate/Environmental"},
    {"name": "Edunation Fund", "focus": "Education/EdTech"},
    {"name": "FinFlow Capital", "focus": "Fintech/Blockchain"}
]

challenges = [
    {
        "title": "AI-Powered Healthcare Diagnosis",
        "description": "Build an AI tool to assist doctors in diagnosing diseases using patient data and real-time imaging."
    },
    {
        "title": "Sustainable Packaging for E-Commerce",
        "description": "Develop eco-friendly packaging solutions that reduce plastic waste and shipping costs."
    },
    {
        "title": "Gamified Education for Underserved Regions",
        "description": "Create a gamified education platform for students with limited internet access."
    }
]

# Existing community ideas (discussion board)
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

# Where we store user pitches to VCs (in-memory)
pitch_submissions = []
# Example structure: {"vc_name": "OpenFound", "pitch": "My idea...", "status": "Pending"}

# Where we store “founders” (mock)
founders_list = [
    {"name": "Alice Johnson", "interests": "Fintech, EdTech"},
    {"name": "Bob Davis", "interests": "AI Healthcare, Climate"},
    {"name": "Catherine Li", "interests": "Blockchain, DevOps"},
]

# --------------------------------------------------------------------------------
# 3. Groq Chat Completion Function
# --------------------------------------------------------------------------------
def generate_ai_ideas(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI that identifies real-world startup problems from research, "
                    "news, and trends. Provide pressing or emerging problems in the domain the user specifies."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error generating response: {e}"

# --------------------------------------------------------------------------------
# 4. Streamlit App
# --------------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Hatcher MVP", layout="wide")

    st.title("Hatcher: Startup Problem + Idea Discovery")
    st.markdown(
        "**Hatcher** is your bridge between market research, idea validation, "
        "and direct investor connections. Explore curated challenges, discover "
        "untapped problems, discuss with peers, and pitch VCs — all in one place."
    )

    # 5 tabs for the new flow
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Discover Problems",
        "VC Challenges",
        "Community Discussion",
        "Network with VCs",
        "Network with Founders"
    ])

    # ----------------------------------------------------------------------------
    # 1) Discover Problems (AI Problem Finder)
    # ----------------------------------------------------------------------------
    with tab1:
        st.header("1. Discover Problems")
        st.markdown("Use AI to uncover **pressing startup problems** in any domain.")

        prompt = st.text_input("What market or tech are you curious about?")
        if st.button("Generate Problems"):
            if prompt.strip():
                with st.spinner("Researching with AI..."):
                    output = generate_ai_ideas(prompt.strip())
                    st.markdown("### Suggested Problems:")
                    st.markdown(output)
            else:
                st.warning("Please enter a market or topic!")

    # ----------------------------------------------------------------------------
    # 2) VC Challenges (Public Startup Problems)
    # ----------------------------------------------------------------------------
    with tab2:
        st.header("2. VC Challenges")
        st.markdown("**VC-curated** challenges. Founders can submit solutions directly.")

        for c in challenges:
            st.markdown(f"### {c['title']}")
            st.write(c['description'])
            st.markdown("---")

    # ----------------------------------------------------------------------------
    # 3) Community Discussion
    # ----------------------------------------------------------------------------
    with tab3:
        st.header("3. Community Discussion")
        st.markdown("Browse or upvote solutions/ideas from the community.")

        # Form to add new idea to the discussion board
        with st.expander("💡 Share a New Idea"):
            title = st.text_input("Idea Title")
            desc = st.text_area("Idea Description")
            tags = st.text_input("Tags (comma-separated)")
            if st.button("Submit Idea"):
                if title and desc:
                    submitted_ideas.append({
                        "title": title,
                        "description": desc,
                        "votes": 0,
                        "investor_backed": False,
                        "tags": [t.strip() for t in tags.split(",") if t.strip()]
                    })
                    st.success("🎉 Your idea was posted!")
                else:
                    st.warning("Please provide both title and description.")

        st.write("---")
        st.subheader("Top Ideas")
        for i, idea in enumerate(submitted_ideas):
            st.markdown(f"**Title:** {idea['title']}")
            st.markdown(f"**Description:** {idea['description']}")
            st.markdown(f"**Tags:** {', '.join(idea['tags'])}")
            st.markdown(f"**Votes:** {idea['votes']}")
            st.markdown(f"**Investor Backed:** {'✅' if idea['investor_backed'] else 'No'}")
            if st.button(f"⬆️ Upvote: {idea['title']}", key=f"vote_{i}"):
                idea['votes'] += 1
                st.success(f"You upvoted '{idea['title']}'")
            st.markdown("---")

    # ----------------------------------------------------------------------------
    # 4) Network with VCs
    # ----------------------------------------------------------------------------
    with tab4:
        st.header("4. Network with VCs")
        st.markdown("Connect with a VC — but first **pitch** them your solution. They must **approve** before you can chat.")

        # Show list of VCs
        st.subheader("Available VCs")
        for vc in vc_list:
            st.write(f"**{vc['name']}** - Focus: {vc['focus']}")

        st.write("---")

        # Pitch form
        st.subheader("Pitch a VC")
        col1, col2 = st.columns(2)
        with col1:
            vc_names = [v["name"] for v in vc_list]
            selected_vc = st.selectbox("Which VC would you like to pitch?", vc_names)

        with col2:
            pitch_text = st.text_area("Your Pitch / Startup Overview")

        if st.button("Submit Pitch"):
            if selected_vc and pitch_text.strip():
                pitch_submissions.append({
                    "vc_name": selected_vc,
                    "pitch": pitch_text.strip(),
                    "status": "Pending"
                })
                st.success(f"Pitch submitted to {selected_vc}! We'll mark it as 'Pending' until they reply.")
            else:
                st.warning("Please select a VC and enter your pitch.")

        st.write("---")

        # Display pitch statuses
        st.subheader("Your Pitch Status")
        if len(pitch_submissions) == 0:
            st.write("No pitches sent yet.")
        else:
            for idx, pitch in enumerate(pitch_submissions):
                st.markdown(f"**VC:** {pitch['vc_name']}")
                st.markdown(f"**Pitch:** {pitch['pitch']}")
                st.markdown(f"**Status:** {pitch['status']}")
                # Mock button for a VC's response
                if pitch['status'] == "Pending":
                    if st.button(f"VC Approves Pitch #{idx+1}", key=f"approve_{idx}"):
                        pitch_submissions[idx]['status'] = "Approved"
                        st.info(f"Pitch #{idx+1} to {pitch['vc_name']} is now Approved. You can chat!")
                st.write("---")

    # ----------------------------------------------------------------------------
    # 5) Network with Founders
    # ----------------------------------------------------------------------------
    with tab5:
        st.header("5. Network with Founders")
        st.markdown("Connect with other founders in your space. (Demo only, no real chat.)")

        st.subheader("Meet Founders")
        for founder in founders_list:
            st.write(f"**{founder['name']}** - Interests: {founder['interests']}")
            if st.button(f"Request Meeting with {founder['name']}"):
                st.info(f"Meeting request sent to {founder['name']}! (Demo placeholder)")

        st.write("---")
        st.markdown("*In a production version, you'd add real chat, calendars, private DMs, etc.*")

if __name__ == "__main__":
    main()
