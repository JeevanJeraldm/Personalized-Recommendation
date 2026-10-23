import streamlit as st
import requests
import re

# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

st.set_page_config(
    page_title="Recommend.AI",
    page_icon="✨",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   MAIN PAGE
========================================================== */

.stApp {
    background: #fff8ef !important;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 35px;
    padding-bottom: 40px;
}


/* ==========================================================
   HEADER
========================================================== */

.hero-title {
    color: #5b21b6 !important;
    font-size: 48px !important;
    font-weight: 800 !important;
    line-height: 1.2;
    margin-bottom: 5px;
}

.hero-subtitle {
    color: #665b6d !important;
    font-size: 18px !important;
}


/* ==========================================================
   SECTION TITLES
========================================================== */

.section-title {
    color: #3b245c !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    margin-top: 25px;
    margin-bottom: 18px;
}


/* ==========================================================
   AI READY
========================================================== */

.status {
    background: #fef3c7 !important;
    color: #92400e !important;
    border-radius: 25px;
    padding: 11px 20px;
    text-align: center;
    font-weight: 800;
    margin-top: 8px;
}


/* ==========================================================
   PROFILE BOX
========================================================== */

.profile-box {
    background: #ffffff !important;
    border: 1px solid #eadcf7;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 6px 20px rgba(91, 33, 182, 0.08);
    margin-bottom: 20px;
}


/* ==========================================================
   LABELS
========================================================== */

label {
    color: #3b245c !important;
    font-weight: 700 !important;
}

[data-testid="stWidgetLabel"] {
    color: #3b245c !important;
}

[data-testid="stWidgetLabel"] p {
    color: #3b245c !important;
    font-weight: 700 !important;
}


/* ==========================================================
   TEXT INPUTS
========================================================== */

div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 1px solid #d8c5ea !important;
    border-radius: 10px !important;
}

div[data-baseweb="input"] > div {
    background-color: #ffffff !important;
}

div[data-baseweb="input"] input {
    background-color: #ffffff !important;
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    font-size: 15px !important;
}


/* ==========================================================
   NUMBER INPUT
========================================================== */

div[data-testid="stNumberInput"] {
    background-color: transparent !important;
}

div[data-testid="stNumberInput"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
}

div[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}


/* ==========================================================
   TEXT AREA
========================================================== */

div[data-baseweb="textarea"] {
    background-color: #ffffff !important;
    border: 1px solid #d8c5ea !important;
    border-radius: 10px !important;
}

div[data-baseweb="textarea"] textarea {
    background-color: #ffffff !important;
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    font-size: 15px !important;
}


/* ==========================================================
   SELECT BOX
========================================================== */

div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #d8c5ea !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: #222222 !important;
}

div[data-baseweb="select"] input {
    color: #222222 !important;
}


/* Dropdown menu */

ul[role="listbox"] {
    background-color: #ffffff !important;
}

li[role="option"] {
    background-color: #ffffff !important;
    color: #222222 !important;
}

li[role="option"]:hover {
    background-color: #f3e8ff !important;
    color: #4c1d95 !important;
}


/* ==========================================================
   GENERATE BUTTON
========================================================== */

div.stButton > button {
    width: 100%;
    min-height: 50px;

    background: linear-gradient(
        90deg,
        #7c3aed,
        #ea580c
    ) !important;

    color: #ffffff !important;

    border: none !important;
    border-radius: 12px !important;

    font-size: 16px !important;
    font-weight: 800 !important;

    box-shadow: 0 5px 15px rgba(124, 58, 237, 0.18);
}

div.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #6d28d9,
        #c2410c
    ) !important;

    color: #ffffff !important;

    transform: translateY(-1px);
}


/* ==========================================================
   RECOMMENDATION CARDS
========================================================== */

.recommendation-card {
    background: #ffffff !important;

    border: 1px solid #eadcf7;
    border-radius: 20px;

    padding: 24px;

    min-height: 210px;

    box-shadow: 0 6px 20px rgba(91, 33, 182, 0.08);

    margin-bottom: 20px;
}

.recommendation-card:hover {
    box-shadow: 0 10px 28px rgba(91, 33, 182, 0.14);
}


.rank {
    color: #ea580c !important;

    font-size: 13px;

    font-weight: 800;

    letter-spacing: 1px;
}


.recommendation-title {
    color: #4c1d95 !important;

    font-size: 21px;

    font-weight: 800;

    margin-top: 10px;

    margin-bottom: 10px;
}


.score {
    color: #c2410c !important;

    font-size: 15px;

    font-weight: 800;
}


.reason {
    color: #665b6d !important;

    font-size: 15px;

    line-height: 1.6;

    margin-top: 12px;
}


/* ==========================================================
   FEEDBACK
========================================================== */

.feedback-box {
    background: #ffffff !important;

    border: 1px solid #eadcf7;

    border-radius: 20px;

    padding: 22px;

    box-shadow: 0 5px 18px rgba(91, 33, 182, 0.07);
}


/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"] {
    background: #2e1745 !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
}


/* ==========================================================
   SUCCESS / WARNING
========================================================== */

div[data-testid="stAlert"] {
    border-radius: 12px;
}


/* ==========================================================
   FOOTER
========================================================== */

.footer {
    text-align: center;

    color: #766b7d !important;

    font-size: 14px;

    padding-top: 10px;
}


/* ==========================================================
   REMOVE EXTRA TOP SPACE
========================================================== */

h1, h2, h3 {
    color: #3b245c !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="
            color:white !important;
            font-size:24px;
        ">
            ✨ Recommend.AI
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            color:#eeeeee !important;
            font-size:15px;
            line-height:1.6;
        ">
            Personalized learning
            recommendation system
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <h3 style="
            color:white !important;
            font-size:18px;
        ">
            📋 Navigation
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write("👤 User Profile")
    st.write("🏆 Recommendations")
    st.write("💬 Feedback")

    st.divider()

    st.markdown(
        """
        <h3 style="
            color:white !important;
            font-size:18px;
        ">
            🤖 AI Engine
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write("Ollama")
    st.write("Llama 3.2")
    st.write("Local AI")

    st.divider()

    st.markdown(
        """
        <p style="
            color:#cfc4d8 !important;
            font-size:13px;
        ">
            Personalized Recommendation System
        </p>

        <p style="
            color:#cfc4d8 !important;
            font-size:13px;
        ">
            Built with Python + Streamlit
        </p>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([5, 1])

with header_left:

    st.markdown(
        '<div class="hero-title">✨ Recommend.AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Personalized learning recommendations powered by Ollama'
        '</div>',
        unsafe_allow_html=True
    )


with header_right:

    st.markdown(
        '<div class="status">🟢 AI Ready</div>',
        unsafe_allow_html=True
    )


# ============================================================
# USER PROFILE
# ============================================================

st.markdown(
    '<div class="section-title">👤 Your Profile</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="profile-box">',
    unsafe_allow_html=True
)


# First row

col1, col2, col3 = st.columns(3)

with col1:

    name = st.text_input(
        "Name",
        value="Jeevan"
    )


with col2:

    age = st.number_input(
        "Age",
        min_value=10,
        max_value=80,
        value=20
    )


with col3:

    field = st.text_input(
        "Field",
        value="Computer Science"
    )


# Second row

col4, col5, col6 = st.columns(3)

with col4:

    interests = st.text_input(
        "Interests",
        value="Artificial Intelligence, Python, Data Science"
    )


with col5:

    level = st.selectbox(
        "Skill Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


with col6:

    preferred = st.selectbox(
        "Preferred Type",
        [
            "Practical",
            "Theoretical",
            "Project-Based",
            "Mixed"
        ]
    )


# Learning goal

goal = st.text_area(
    "🎯 Learning Goal",
    value="I want to learn Artificial Intelligence through practical courses.",
    height=100
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# GENERATE RECOMMENDATIONS
# ============================================================

st.write("")

generate = st.button(
    "✨ Generate My Recommendations",
    use_container_width=True
)


if generate:

    prompt = f"""
You are an intelligent personalized recommendation assistant.

Analyze the following user profile and generate exactly
5 personalized learning recommendations.

USER PROFILE

Name: {name}
Age: {age}
Field: {field}
Interests: {interests}
Skill Level: {level}
Preferred Learning Type: {preferred}
Learning Goal: {goal}

REQUIREMENTS

1. Recommend learning courses, topics, or skills.
2. Match recommendations with the user's interests.
3. Consider the user's skill level.
4. Consider the preferred learning type.
5. Consider the learning goal.
6. Give a match score between 80% and 99%.
7. Give a short reason for every recommendation.
8. Rank recommendations from best match to lowest match.
9. Return exactly 5 recommendations.

Use this exact format:

1. Python for AI | Score: 95% | Reason: Matches the user's interest in Python and Artificial Intelligence.
2. Machine Learning Basics | Score: 92% | Reason: Suitable for a beginner interested in AI.
3. Generative AI | Score: 89% | Reason: Directly supports the user's AI learning goal.
4. Data Science with Python | Score: 86% | Reason: Combines Python and Data Science interests.
5. Deep Learning Basics | Score: 83% | Reason: Provides a natural progression after machine learning.

Return ONLY the five recommendations.
"""

    with st.spinner("🤖 Analyzing your profile..."):

        try:

            response = requests.post(
                OLLAMA_URL,

                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                },

                timeout=180
            )

            response.raise_for_status()

            result = response.json()["response"].strip()

            st.session_state["recommendations"] = result

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to Ollama. "
                "Please make sure Ollama is running."
            )

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )


# ============================================================
# DISPLAY RECOMMENDATIONS
# ============================================================

if "recommendations" in st.session_state:

    st.markdown(
        '<div class="section-title">'
        '🏆 Personalized For You'
        '</div>',
        unsafe_allow_html=True
    )

    raw_result = st.session_state["recommendations"]

    lines = [
        line.strip()
        for line in raw_result.splitlines()
        if line.strip()
    ]

    recommendations = []


    # Parse recommendations

    for line in lines:

        match = re.match(
            r"^\d+\.\s*(.*?)\s*\|\s*Score:\s*(\d+)%\s*\|\s*Reason:\s*(.*)$",
            line,
            re.IGNORECASE
        )

        if match:

            title = match.group(1).strip()

            score = match.group(2).strip()

            reason = match.group(3).strip()

            recommendations.append(
                (
                    title,
                    score,
                    reason
                )
            )


    # ========================================================
    # RECOMMENDATION CARDS
    # ========================================================

    if recommendations:

        for start in range(
            0,
            len(recommendations),
            3
        ):

            current = recommendations[
                start:start + 3
            ]

            columns = st.columns(
                len(current)
            )

            for i, (title, score, reason) in enumerate(
                current
            ):

                with columns[i]:

                    rank_number = start + i + 1

                    st.markdown(
                        f"""
                        <div class="recommendation-card">

                            <div class="rank">
                                #{rank_number}
                                RECOMMENDATION
                            </div>

                            <div class="recommendation-title">
                                {title}
                            </div>

                            <div class="score">
                                ⭐ {score}% MATCH
                            </div>

                            <div class="reason">
                                <b>Why:</b>
                                {reason}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    else:

        st.markdown(
            raw_result
        )


    # ========================================================
    # FEEDBACK SECTION
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '💬 Refine Your Recommendations'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="feedback-box">',
        unsafe_allow_html=True
    )

    feedback = st.text_area(
        "Tell the AI what you would like to change:",

        placeholder=(
            "Example: I am more interested in "
            "AI than Web Development."
        ),

        height=110
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")


    # ========================================================
    # UPDATE RECOMMENDATIONS
    # ========================================================

    update = st.button(
        "🔄 Update Recommendations",
        use_container_width=True
    )


    if update:

        if not feedback.strip():

            st.warning(
                "⚠️ Please enter your feedback first."
            )

        else:

            update_prompt = f"""
You are an intelligent personalized recommendation assistant.

USER PROFILE

Interests: {interests}
Skill Level: {level}
Preferred Learning Type: {preferred}
Learning Goal: {goal}

CURRENT RECOMMENDATIONS

{st.session_state["recommendations"]}

USER FEEDBACK

{feedback}

TASK

Update the recommendations according to the
user's feedback.

Generate exactly 5 NEW personalized
learning recommendations.

REQUIREMENTS

1. Give priority to the user's new feedback.
2. Still consider the original user profile.
3. Rank recommendations from best match to lowest match.
4. Give a score between 80% and 99%.
5. Give a short reason.
6. Return exactly 5 recommendations.

Use EXACTLY this format:

1. Recommendation | Score: 95% | Reason: Short explanation.
2. Recommendation | Score: 92% | Reason: Short explanation.
3. Recommendation | Score: 89% | Reason: Short explanation.
4. Recommendation | Score: 86% | Reason: Short explanation.
5. Recommendation | Score: 83% | Reason: Short explanation.

Return ONLY the five recommendations.
"""

            with st.spinner(
                "🔄 Updating your recommendations..."
            ):

                try:

                    response = requests.post(
                        OLLAMA_URL,

                        json={
                            "model": MODEL,
                            "prompt": update_prompt,
                            "stream": False
                        },

                        timeout=180
                    )

                    response.raise_for_status()

                    updated_result = (
                        response
                        .json()["response"]
                        .strip()
                    )

                    st.session_state[
                        "recommendations"
                    ] = updated_result

                    st.success(
                        "✅ Recommendations updated "
                        "based on your feedback!"
                    )

                    st.rerun()

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Could not connect to Ollama."
                    )

                except Exception as e:

                    st.error(
                        f"❌ Error: {e}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        ✨ Recommend.AI &nbsp; | &nbsp;
        Powered by Ollama + Llama 3.2 &nbsp; | &nbsp;
        Personalized Recommendation System
    </div>
    """,
    unsafe_allow_html=True
)