import streamlit as st
import requests
import os
import random

# NEW LINES FOR TINYDB
from tinydb import TinyDB, Query

# Ensure db folder exists
os.makedirs("db", exist_ok=True)
db = TinyDB("db/pitches.json")

# --------------------------------------------------------------------------------
# 1. Groq API Setup (Hard-coded for DEMO — in production, store in st.secrets!)
# --------------------------------------------------------------------------------
GROQ_API_KEY = "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"  # Replace with your actual key
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
# Example structure: {"founder_name": "Alice", "vc_name": "OpenFound", "pitch": "My idea...", "status": "Pending"}

founders_list = [
    {"name": "Alice Johnson", "interests": "Fintech, EdTech"},
    {"name": "Bob Davis", "interests": "AI Healthcare, Climate"},
    {"name": "Catherine Li", "interests": "Blockchain, DevOps"},
]

# --------------------------------------------------------------------------------
# 3. Helper Functions
# --------------------------------------------------------------------------------
def generate_ai_ideas(prompt):
    """ Calls Groq AI to generate a list of real-world problems in the given domain. """
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
                    "news, and trends. Provide pressing or emerging problems in the domain specified."
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

def analyze_pitches_with_ai(all_pitches_text):
    """ Let the VC use AI to analyze all pending pitches. """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = (
        "You are a VC analyzing these pitches. Summarize each pitch, evaluate potential, "
        "and recommend accept/reject with a short reason:\n\n" + all_pitches_text
    )
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a thorough, analytical VC assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 500
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error analyzing pitches: {e}"

# NEW HELPER: Save pitch to TinyDB
def save_pitch_to_db(founder, vc, pitch_text):
    """ Persist pitch to TinyDB so we don't lose it. """
    PitchTable = db.table("pitches")
    PitchTable.insert({
        "founder_name": founder,
        "vc_name": vc,
        "pitch": pitch_text,
        "status": "Pending"
    })

def get_all_pitches_from_db():
    """ Return all pitches from TinyDB. """
    PitchTable = db.table("pitches")
    return PitchTable.all()

def update_pitch_status_in_db(founder, pitch_text, new_status):
    """ Update pitch status in TinyDB. """
    PitchTable = db.table("pitches")
    query = Query()
    PitchTable.update(
        {"status": new_status},
        (query.founder_name == founder) & (query.pitch == pitch_text)
    )

# --------------------------------------------------------------------------------
# 4. Streamlit App
# --------------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Hatcher MVP", layout="wide")

    # ---------------------------------------------------------------------
    # 4A. Simple Mock Login
    # ---------------------------------------------------------------------
    st.title("Hatcher: Problems for Solutions")
    role = st.sidebar.selectbox("Login as:", ["Aspiring Founder", "VC"])
    user_name = st.sidebar.text_input("Enter your Name (mock)")
    st.sidebar.write("This is just a demo login — no real auth.")

    # If no user name yet, show a minimal prompt
    if not user_name.strip():
        st.warning("Please enter your name in the sidebar to continue.")
        return  # Stop rendering until user enters a name

    st.markdown(
        f"**Currently logged in as:** `{user_name}` — **Role:** `{role}`\n\n"
        "This is a mock login flow for demonstration."
    )

    # Show instructions at top
    st.markdown(
        "**Hatcher** is your bridge between market research, idea validation, "
        "and direct investor connections."
    )

    # 5 or 6 tabs depending on role
    if role == "Aspiring Founder":
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Discover Problems",
            "VC Challenges",
            "Community Discussion",
            "Pitch to VCs",
            "Network with Founders"
        ])

        # ----------------------------------------------------------------
        # Founder Tab 1: Discover Problems
        # ----------------------------------------------------------------
        with tab1:
            st.header("Discover Problems")
            prompt = st.text_input("What market or tech are you curious about?")
            if st.button("Generate Problems"):
                if prompt.strip():
                    with st.spinner("Researching with AI..."):
                        output = generate_ai_ideas(prompt.strip())
                        st.markdown("### Suggested Problems:")
                        st.markdown(output)
                else:
                    st.warning("Please enter a market or topic!")

        # ----------------------------------------------------------------
        # Founder Tab 2: VC Challenges
        # ----------------------------------------------------------------
        with tab2:
            st.header("VC Challenges")
            st.markdown("**VC-curated** problems open for founder solutions.")

            for c in challenges:
                st.markdown(f"### {c['title']}")
                st.write(c['description'])
                st.markdown("---")

        # ----------------------------------------------------------------
        # Founder Tab 3: Community Discussion
        # ----------------------------------------------------------------
        with tab3:
            st.header("Community Discussion")
            st.markdown("Browse or upvote solutions/ideas from the community.")

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

        # ----------------------------------------------------------------
        # Founder Tab 4: Pitch to VCs
        # ----------------------------------------------------------------
        with tab4:
            st.header("Pitch to VCs")
            st.markdown("Select a VC to pitch. They must approve before you can chat further.")

            # Show list of VCs
            st.subheader("Available VCs")
            for vc in vc_list:
                st.write(f"**{vc['name']}** - Focus: {vc['focus']}")

            st.write("---")
            st.subheader("Submit Your Pitch")
            col1, col2 = st.columns(2)
            with col1:
                vc_names = [v["name"] for v in vc_list]
                selected_vc = st.selectbox("Which VC would you like to pitch?", vc_names)
            with col2:
                pitch_text = st.text_area("Your Pitch / Startup Overview")

            if st.button("Submit Pitch"):
                if selected_vc and pitch_text.strip():
                    # Existing In-Memory
                    pitch_submissions.append({
                        "founder_name": user_name,
                        "vc_name": selected_vc,
                        "pitch": pitch_text.strip(),
                        "status": "Pending"
                    })
                    # NEW: Save to TinyDB
                    save_pitch_to_db(user_name, selected_vc, pitch_text.strip())

                    st.success(f"Pitch submitted to {selected_vc}! We'll mark it as 'Pending' until they reply.")
                else:
                    st.warning("Please select a VC and enter your pitch.")

            # Show your pitches and statuses
            st.write("---")
            st.subheader("Your Pitch Status")
            my_pitches_mem = [p for p in pitch_submissions if p["founder_name"] == user_name]
            # Also load from DB in case we want to show them
            all_db_pitches = get_all_pitches_from_db()
            my_pitches_db = [p for p in all_db_pitches if p["founder_name"] == user_name]

            # Combine them or just show memory for the demo
            if len(my_pitches_mem) == 0 and len(my_pitches_db) == 0:
                st.write("No pitches sent yet.")
            else:
                st.markdown("**Pitches (In-Memory):**")
                for idx, pitch in enumerate(my_pitches_mem):
                    st.markdown(f"**VC:** {pitch['vc_name']}")
                    st.markdown(f"**Pitch:** {pitch['pitch']}")
                    st.markdown(f"**Status:** {pitch['status']}")
                    st.write("---")

                st.markdown("**Pitches (Saved in TinyDB):**")
                for idx, pitch in enumerate(my_pitches_db):
                    st.markdown(f"**VC:** {pitch['vc_name']}")
                    st.markdown(f"**Pitch:** {pitch['pitch']}")
                    st.markdown(f"**Status:** {pitch['status']}")
                    st.write("---")

        # ----------------------------------------------------------------
        # Founder Tab 5: Network with Founders
        # ----------------------------------------------------------------
        with tab5:
            st.header("Network with Founders")
            st.markdown("Connect with other founders in your space. (Demo only, no real chat.)")

            st.subheader("Meet Founders")
            for founder in founders_list:
                st.write(f"**{founder['name']}** - Interests: {founder['interests']}")
                if founder['name'] != user_name:
                    if st.button(f"Request Meeting with {founder['name']}"):
                        st.info(f"Meeting request sent to {founder['name']}! (Demo placeholder)")

            st.write("---")
            st.markdown("*In a real app, you'd add chat, scheduling, or DMs.*")

    # ==============================================================================
    # IF VC LOGIN
    # ==============================================================================
    else:
        # role == "VC"
        tabA, tabB, tabC = st.tabs([
            "Analyze Pitches",
            "Challenges & Community Ideas",
            "Founders Directory"
        ])

        # ----------------------------------------------------------------
        # VC Tab A: Analyze & Approve Pitches
        # ----------------------------------------------------------------
        with tabA:
            st.header("Analyze Incoming Pitches")
            st.write("View all founder-submitted pitches, approve or reject them, or use AI to get analysis.")

            # Merge old in-memory with DB
            all_db = get_all_pitches_from_db()
            # Filter only those addressed to this VC
            pending_pitches_db = [p for p in all_db if p["vc_name"] == user_name]

            # Show all pitches (from in-memory + DB)
            # We'll unify with the existing memory approach:
            combined_in_mem = [p for p in pitch_submissions if p["vc_name"] == user_name]
            # Merge them (in real code you'd unify or rely solely on DB)
            combined_all = combined_in_mem + pending_pitches_db

            # Remove duplicates (just in case):
            unique_pitches = []
            seen = set()
            for p in combined_all:
                signature = (p["founder_name"], p["vc_name"], p["pitch"])
                if signature not in seen:
                    unique_pitches.append(p)
                    seen.add(signature)

            if len(unique_pitches) == 0:
                st.write("No pitches to analyze yet.")
            else:
                # Option: Use AI to summarize all
                if st.button("Use AI to Summarize & Filter All Pitches"):
                    with st.spinner("Analyzing with AI..."):
                        text_for_ai = "\n\n".join([
                            f"Founder: {p['founder_name']}\nPitch: {p['pitch']}\nCurrentStatus: {p['status']}"
                            for p in unique_pitches
                        ])
                        ai_feedback = analyze_pitches_with_ai(text_for_ai)
                        st.markdown("### AI Feedback & Recommendations")
                        st.write(ai_feedback)

                        # NEW: Made-Up Additional Analysis
                        total_pitches = len(unique_pitches)
                        best_pitch = random.choice(unique_pitches)
                        st.markdown(f"**We found {total_pitches} total pitches.**")
                        st.markdown(f"**Random 'Best Pitch':** {best_pitch['pitch']} from Founder {best_pitch['founder_name']}")
                        st.markdown("*(This is a made-up analysis for demonstration!)*")

                st.write("---")
                # Now display each pitch with Approve/Reject
                for idx, pitch in enumerate(unique_pitches):
                    st.markdown(f"**From:** {pitch['founder_name']}")
                    st.markdown(f"**Pitch:** {pitch['pitch']}")
                    status_text = pitch.get("status", "Pending")
                    st.markdown(f"**Status:** {status_text}")

                    if status_text == "Pending":
                        if st.button(f"Approve Pitch #{idx+1}", key=f"approve_{idx}"):
                            pitch["status"] = "Approved"
                            # Update DB as well
                            update_pitch_status_in_db(pitch["founder_name"], pitch["pitch"], "Approved")
                            st.success(f"Approved Pitch #{idx+1}")
                        if st.button(f"Reject Pitch #{idx+1}", key=f"reject_{idx}"):
                            pitch["status"] = "Rejected"
                            update_pitch_status_in_db(pitch["founder_name"], pitch["pitch"], "Rejected")
                            st.warning(f"Rejected Pitch #{idx+1}")
                    else:
                        st.info(f"Pitch is already {status_text}")
                    st.write("---")

        # ----------------------------------------------------------------
        # VC Tab B: Challenges & Community
        # ----------------------------------------------------------------
        with tabB:
            st.header("VC Challenges & Community Ideas")
            st.markdown("Here are the public challenges and community ideas. (Read-only for this demo.)")

            st.subheader("Your Public Challenges")
            for c in challenges:
                st.markdown(f"### {c['title']}")
                st.write(c['description'])
                st.markdown("---")

            st.subheader("Community Ideas")
            for idea in submitted_ideas:
                st.markdown(f"**Title:** {idea['title']}")
                st.markdown(f"**Description:** {idea['description']}")
                st.markdown(f"**Votes:** {idea['votes']}")
                st.markdown(f"**Investor Backed:** {'✅' if idea['investor_backed'] else 'No'}")
                st.markdown("---")

        # ----------------------------------------------------------------
        # VC Tab C: Founders Directory
        # ----------------------------------------------------------------
        with tabC:
            st.header("Founders Directory")
            st.markdown("Browse potential founders. (Demo only.)")

            for founder in founders_list:
                st.markdown(f"**{founder['name']}** — Interests: {founder['interests']}")
            st.write("---")
            st.markdown("*In a real app, you'd add direct chat or scheduling with these founders.*")

if __name__ == "__main__":
    main()
