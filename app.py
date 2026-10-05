import streamlit as st
import pandas as pd
import os
from chatbot import CollegeBot
import risk


# =========================================================
# PAGE CONFIGURATION
# =========================================================

COLLEGE = "V.S.B Engineering College"

st.set_page_config(
    page_title="V.S.B Engineering College | Campus AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Welcome card */
    .welcome-card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }

    /* Info cards */
    .info-card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        min-height: 130px;
    }

    .info-title {
        font-size: 16px;
        font-weight: 600;
    }

    .info-text {
        color: #64748b;
        font-size: 14px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 40px;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTIONS
# =========================================================

def get_bot():
    return CollegeBot()


@st.cache_resource
def get_risk():
    return risk.load()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:10px;">
            <div style="font-size:48px;">🎓</div>
            <h2 style="margin-bottom:0;">Campus AI</h2>
            <p style="color:#cbd5e1;">Smart College Assistant</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "💬 Campus Chatbot",
            "🚨 Student Risk Dashboard",
            "📊 Analytics",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.markdown(
        f"""
        <div style="text-align:center;">
            <b>{COLLEGE}</b><br>
            <span style="color:#cbd5e1;">
            AI & DS Final Year Project
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CHATBOT
# =========================================================

if page.startswith("💬"):

    st.markdown(
        '<div class="main-title">💬 College Enquiry Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Ask questions about admissions, courses, fees, hostel, '
        'attendance, exams and placements.'
        '</div>',
        unsafe_allow_html=True
    )

    # Welcome card
    st.markdown(
        """
        <div class="welcome-card">
            <h3>👋 Vanakkam!</h3>
            <p>
            Welcome to the V.S.B Engineering College AI Enquiry Assistant.
            </p>
            <p style="color:#64748b;">
            You can ask in English or Tanglish.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick questions
    st.markdown("### ⚡ Quick Questions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("🎓 Courses", use_container_width=True):
            st.session_state.quick_question = "VSB la enna courses iruku?"

    with q2:
        if st.button("💰 Fees", use_container_width=True):
            st.session_state.quick_question = "VSB la fees evlo?"

    with q3:
        if st.button("🏠 Hostel", use_container_width=True):
            st.session_state.quick_question = "hostel facility iruka?"

    with q4:
        if st.button("💼 Placements", use_container_width=True):
            st.session_state.quick_question = "VSB placement la enna companies varanga?"

    st.divider()

    # Chat history
    if "msgs" not in st.session_state:

        st.session_state.msgs = [
            (
                "assistant",
                "Vanakkam! 👋 College pathi enna therinjukanum?",
                None
            )
        ]

    # Clear chat
    col1, col2 = st.columns([6, 1])

    with col2:

        if st.button("🗑️ Clear", use_container_width=True):

            st.session_state.msgs = [
                (
                    "assistant",
                    "Vanakkam! 👋 College pathi enna therinjukanum?",
                    None
                )
            ]

            st.session_state.pop(
                "quick_question",
                None
            )

            st.rerun()

    # Display messages
    for role, text, src in st.session_state.msgs:

        with st.chat_message(role):

            st.write(text)

            if src:
                st.caption(
                    f"📄 Source: {src}"
                )

    # Input
    q = st.chat_input(
        "Type your question..."
    )

    # Quick question handling
    if "quick_question" in st.session_state:

        q = st.session_state.pop(
            "quick_question"
        )

    if q:

        st.session_state.msgs.append(
            (
                "user",
                q,
                None
            )
        )

        bot = get_bot()

        res = bot.ask(q)

        src = None

        if res["hits"]:

            src = (
                f"{res['hits'][0][1]}  |  "
                f"confidence "
                f"{res['confidence'] * 100:.0f}%"
            )

        st.session_state.msgs.append(
            (
                "assistant",
                res["answer"],
                src
            )
        )

        st.rerun()


# =========================================================
# STUDENT RISK DASHBOARD
# =========================================================

elif page.startswith("🚨"):

    st.markdown(
        '<div class="main-title">🚨 Student Risk Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Identify students who may need early mentor intervention.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="welcome-card">
            <h3>📋 Upload Student Data</h3>
            <p>
            Upload a CSV file containing attendance, study hours,
            previous marks, assignments and other student factors.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    f = st.file_uploader(
        "Upload class CSV",
        type="csv"
    )

    if (
        f is None
        and os.path.exists(
            "data/sample_class.csv"
        )
    ):

        if st.checkbox(
            "Use sample class data",
            value=True
        ):

            f = "data/sample_class.csv"

    if f is not None:

        df = pd.read_csv(f)

        missing = [
            c
            for c in risk.FEATURES
            if c not in df.columns
        ]

        if missing:

            st.error(
                f"Missing columns: {missing}"
            )

        else:

            if "name" not in df.columns:

                df["name"] = [
                    f"Student {i + 1}"
                    for i in range(len(df))
                ]

            out = risk.analyse(
                df,
                get_risk()
            )

            st.markdown("### 📊 Risk Summary")

            a, b, c, d = st.columns(4)

            a.metric(
                "👥 Total Students",
                len(out)
            )

            b.metric(
                "🔴 High Risk",
                int(
                    (out.risk_level == "High").sum()
                )
            )

            c.metric(
                "🟠 Medium Risk",
                int(
                    (out.risk_level == "Medium").sum()
                )
            )

            d.metric(
                "🟢 Low Risk",
                int(
                    (out.risk_level == "Low").sum()
                )
            )

            st.divider()

            level = st.multiselect(
                "Filter Risk Level",
                [
                    "High",
                    "Medium",
                    "Low"
                ],
                default=[
                    "High",
                    "Medium"
                ]
            )

            shown = out[
                out.risk_level.isin(level)
            ]

            st.dataframe(
                shown[
                    [
                        "name",
                        "fail_risk_%",
                        "risk_level",
                        "main_reasons",
                        "suggested_action"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇️ Download Mentor Report",
                shown.to_csv(index=False),
                "mentor_report.csv",
                use_container_width=True
            )

            st.markdown(
                "### 📈 Student Risk Distribution"
            )

            st.bar_chart(
                out.set_index("name")[
                    "fail_risk_%"
                ].head(15)
            )


# =========================================================
# ANALYTICS
# =========================================================

elif page.startswith("📊"):

    st.markdown(
        '<div class="main-title">📊 Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Model performance and chatbot usage analytics.'
        '</div>',
        unsafe_allow_html=True
    )

    t1, t2 = st.tabs(
        [
            "🤖 Model Comparison",
            "💬 Chatbot Usage"
        ]
    )

    with t1:

        bd = get_risk()

        st.markdown(
            f"""
            <div class="welcome-card">
                <h3>🏆 Best Model</h3>
                <p>
                <b>{bd['name']}</b>
                </p>
                <p style="color:#64748b;">
                Selected based on ROC-AUC performance.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            bd["table"],
            hide_index=True,
            use_container_width=True
        )

        if bd["importance"] is not None:

            st.markdown(
                "### 📌 Feature Importance"
            )

            st.bar_chart(
                pd.Series(
                    bd["importance"],
                    index=risk.FEATURES
                )
            )

    with t2:

        if os.path.exists(
            "logs/queries.csv"
        ):

            lg = pd.read_csv(
                "logs/queries.csv"
            )

            a, b = st.columns(2)

            a.metric(
                "💬 Questions Asked",
                len(lg)
            )

            b.metric(
                "❓ Unanswered",
                int(
                    (lg.source == "none").sum()
                )
            )

            st.markdown(
                "### 📚 Most Asked Topics"
            )

            st.bar_chart(
                lg.source.value_counts()
            )

            st.dataframe(
                lg.tail(20),
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "No questions yet. "
                "Ask something in the chatbot first."
            )


# =========================================================
# ABOUT
# =========================================================

else:

    st.markdown(
        '<div class="main-title">ℹ️ About Campus AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'AI-powered college information and student support system.'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">
                    💬 RAG Enquiry Chatbot
                </div>
                <br>
                <div class="info-text">
                    Answers college-related questions using
                    a college-specific knowledge base with
                    TF-IDF retrieval and source-based responses.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">
                    🚨 Early Warning System
                </div>
                <br>
                <div class="info-text">
                    Analyses student academic factors and
                    identifies students who may need
                    mentor intervention.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">
                    📊 Analytics
                </div>
                <br>
                <div class="info-text">
                    Provides model comparison, feature
                    importance and chatbot usage statistics.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">
                    🎓 Project
                </div>
                <br>
                <div class="info-text">
                    V.S.B Engineering College<br>
                    AI & DS Final Year Project
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        V.S.B Engineering College • Campus AI Assistant<br>
        AI & DS Final Year Project
    </div>
    """,
    unsafe_allow_html=True
)