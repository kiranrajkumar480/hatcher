import streamlit as st
import requests

# --- 1. Groq API Setup ------------------------------------------------------------
GROQ_API_KEY = "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" # Add this in Streamlit Cloud Secrets
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- 2. Mock Data ------------------------------------------------------------------
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

# --- 3. Groq Chat Completion Function ----------------------------------------------
def generate_ai_ideas(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are an AI that identifies real-world startup problems from research, news, and trends."},
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

# --- 4. Streamlit App Layout --------------------------------------------------------
def main():
    st.set_page_config(page_title="Hatcher MVP", layout="wide")

    st.title("Hatcher: Startup Problem + Idea Discovery")
    st.markdown("""
        **Hatcher** helps anyone go from market research to investor connection:
        - Discover real, AI-validated problems
        - Submit and upvote creative solutions
        - Let VCs post challenges and track ideas
        - Use Hatcher as a bridge between builders and funders
    """)

    st.sidebar.title("🔍 VC Profiles")
    for vc in vc_list:
        st.sidebar.markdown(f"- **{vc['name']}** ({vc['focus']})")

    st.sidebar.title("💡 Submit Your Solution")
    with st.sidebar.form("submit_form", clear_on_submit=True):
        title = st.text_input("Title")
        desc = st.text_area("Description")
        tags = st.text_input("Tags (comma-separated)")
        submit = st.form_submit_button("Submit")
        if submit and title and desc:
            submitted_ideas.append({
                "title": title,
                "description": desc,
                "votes": 0,
                "investor_backed": False,
                "tags": [t.strip() for t in tags.split(",") if t.strip()]
            })
            st.success("🎉 Your idea was submitted!")

    tab1, tab2, tab3 = st.tabs(["🔍 Discover Problems", "📢 VC Challenges", "🚀 Community Ideas"])

    with tab1:
        st.header("AI Problem Finder")
        prompt = st.text_input("What market or tech are you curious about?", key="ai_input")
        if st.button("Find Problems", key="ai_button"):
            if prompt.strip():
                with st.spinner("Researching with AI..."):
                    output = generate_ai_ideas(prompt)
                    st.markdown("### Suggested Problems:")
                    st.markdown(output)
            else:
                st.warning("Please enter a market or topic!")

    with tab2:
        st.header("VC-Published Startup Challenges")
        for c in challenges:
            st.markdown(f"### {c['title']}")
            st.write(c['description'])
            st.markdown("---")

    with tab3:
        st.header("Top Community Ideas")
        for i, idea in enumerate(submitted_ideas):
            st.markdown(f"**Title:** {idea['title']}")
            st.markdown(f"**Description:** {idea['description']}")
            st.markdown(f"**Tags:** {', '.join(idea['tags'])}")
            st.markdown(f"**Votes:** {idea['votes']}")
            st.markdown(f"**Investor Backed:** {'✅' if idea['investor_backed'] else 'No'}")
            if st.button(f"⬆️ Upvote", key=f"vote_{i}"):
                idea['votes'] += 1
                st.success(f"You upvoted '{idea['title']}'")
            st.markdown("---")

if __name__ == "__main__":
    main()
