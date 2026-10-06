import os
import io
import pandas as pd
import streamlit as st

from chatbot import CollegeBot
import risk

st.set_page_config(
    page_title="Campus AI | V.S.B Engineering College",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
<style>
.stApp {
    background-color: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #111827;
}

.subtitle {
    font-size: 17px;
    color: #4b5563;
    margin-bottom: 20px;
}

[data-testid="stChatMessage"] {
    background-color: white !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 14px !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong {
    color: #111827 !important;
}

[data-testid="stChatInput"] textarea {
    color: #111827 !important;
    background-color: white !important;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #4b5563 !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
}

.footer-text {
    text-align: center;
    color: #6b7280;
    font-size: 14px;
    padding-top: 25px;
}

.about-title {
    font-size: 36px;
    font-weight: 800;
    color: #111827 !important;
    margin-bottom: 18px;
}

.about-intro {
    background-color: #dbeafe;
    color: #1e3a8a !important;
    padding: 22px 26px;
    border-radius: 14px;
    font-size: 17px;
    line-height: 1.7;
    border: 1px solid #bfdbfe;
    margin-bottom: 28px;
}

.about-intro b {
    color: #1e3a8a !important;
}

.about-section {
    background-color: white;
    padding: 24px 28px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.about-heading {
    font-size: 25px;
    font-weight: 750;
    color: #111827 !important;
    margin-bottom: 18px;
}

.about-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

.about-list div {
    color: #374151 !important;
    font-size: 16px;
    padding: 10px 12px;
    background-color: #f9fafb;
    border-radius: 9px;
}

.about-list b {
    color: #111827 !important;
}

.about-text {
    color: #374151 !important;
    font-size: 16px;
    line-height: 1.7;
}

.about-text b {
    color: #111827 !important;
}

.tech-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

.tech-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
}

.tech-icon {
    font-size: 27px;
}

.tech-name {
    color: #6b7280 !important;
    font-size: 13px;
    margin-bottom: 3px;
}

.tech-value {
    color: #111827 !important;
    font-size: 16px;
    font-weight: 700;
}

.about-footer {
    text-align: center;
    color: #6b7280 !important;
    font-size: 14px;
    line-height: 1.7;
    padding: 20px 0 10px 0;
}

.about-footer b {
    color: #374151 !important;
}

@media (max-width: 768px) {
    .about-list {
        grid-template-columns: 1fr;
    }

    .tech-grid {
        grid-template-columns: 1fr;
    }

    .about-title {
        font-size: 30px;
    }
}
</style>
""",
    unsafe_allow_html=True
)


@st.cache_resource
def get_bot():
    return CollegeBot()


@st.cache_resource
def get_risk_model():
    try:
        return risk.load()
    except Exception:
        return None


def load_sample_data():
    path = os.path.join(
        "data",
        "sample_class.csv"
    )

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def create_excel_file(df):
    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Risk Report"
        )

    output.seek(0)

    return output


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:

    st.markdown("## 🎓 Campus AI")

    st.caption("Smart College Assistant")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "💬 Campus Chatbot",
            "🚨 Student Risk Dashboard",
            "📊 Analytics",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.caption("V.S.B Engineering College")
    st.caption("AI & DS Final Year Project")


if page == "💬 Campus Chatbot":

    st.markdown(
        '<div class="main-title">💬 College Enquiry Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Ask questions about admissions, courses, fees, hostel, '
        'attendance, exams, placements and more.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "👋 Vanakkam!\n\n"
        "Welcome to the V.S.B Engineering College AI Enquiry Assistant.\n\n"
        "You can ask questions in English or Tanglish."
    )

    st.markdown("### ⚡ Quick Questions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            "📚 Courses",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "VSB la enna courses iruku?"
                }
            )

            st.rerun()

    with col2:

        if st.button(
            "💰 Fees",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "VSB la fees evlo?"
                }
            )

            st.rerun()

    with col3:

        if st.button(
            "🏠 Hostel",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "VSB la hostel iruka?"
                }
            )

            st.rerun()

    with col4:

        if st.button(
            "💼 Placements",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "VSB placement epdi iruku?"
                }
            )

            st.rerun()

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

            if message["role"] == "assistant":

                source = message.get(
                    "source",
                    ""
                )

                confidence = message.get(
                    "confidence",
                    ""
                )

                if source or confidence:

                    details = ""

                    if source:
                        details += f"📄 Source: {source}"

                    if confidence:

                        if details:
                            details += " | "

                        details += (
                            f"Confidence: {confidence}"
                        )

                    st.caption(details)

    user_question = st.chat_input(
        "Ask about V.S.B Engineering College..."
    )

    if user_question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        bot = get_bot()

        try:

            result = bot.ask(
                user_question
            )

        except Exception:

            try:

                result = bot.get_answer(
                    user_question
                )

            except Exception as error:

                result = {
                    "answer": (
                        "Sorry, chatbot error occurred: "
                        + str(error)
                    ),
                    "confidence": 0,
                    "hits": []
                }

        answer = ""
        source = ""
        confidence = ""

        if isinstance(result, dict):

            answer = result.get(
                "answer",
                result.get(
                    "response",
                    ""
                )
            )

            confidence = result.get(
                "confidence",
                ""
            )

            source = result.get(
                "source",
                result.get(
                    "file",
                    ""
                )
            )

            if not source:

                hits = result.get(
                    "hits",
                    []
                )

                if hits:

                    first_hit = hits[0]

                    if isinstance(
                        first_hit,
                        (list, tuple)
                    ):

                        if len(first_hit) >= 2:
                            source = first_hit[1]

                        if (
                            not confidence
                            and len(first_hit) >= 3
                        ):
                            confidence = first_hit[2]

        elif isinstance(result, tuple):

            if len(result) >= 1:
                answer = result[0]

            if len(result) >= 2:
                source = result[1]

            if len(result) >= 3:
                confidence = result[2]

        else:

            answer = str(result)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": str(answer),
                "source": str(source),
                "confidence": str(confidence)
            }
        )

        st.rerun()

    if st.session_state.messages:

        if st.button("🗑️ Clear Chat"):

            st.session_state.messages = []

            st.rerun()

    st.divider()

    st.caption(
        "V.S.B Engineering College • Campus AI Assistant • AI & DS Final Year Project"
    )


elif page == "🚨 Student Risk Dashboard":

    st.markdown(
        '<div class="main-title">🚨 Student Risk Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Identify students who may require academic mentoring.'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Student CSV",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(
            uploaded_file
        )

    else:

        df = load_sample_data()

        st.info(
            "Showing sample student data. "
            "Upload your own CSV to analyse students."
        )

    if df.empty:

        st.warning(
            "No student data available."
        )

    else:

        risk_df = df.copy()

        model = get_risk_model()

        if model is not None:

            try:

                if hasattr(
                    model,
                    "predict"
                ):

                    numeric_df = (
                        risk_df.select_dtypes(
                            include=["number"]
                        )
                    )

                    if not numeric_df.empty:

                        predictions = model.predict(
                            numeric_df
                        )

                        if len(predictions) == len(
                            risk_df
                        ):

                            risk_df["Risk"] = predictions

            except Exception:

                pass

        risk_column = None

        for column in risk_df.columns:

            if column.lower() in [
                "risk",
                "risk_level",
                "risk level"
            ]:

                risk_column = column
                break

        if risk_column:

            values = (
                risk_df[risk_column]
                .astype(str)
                .str.lower()
            )

            high_count = values.str.contains(
                "high"
            ).sum()

            medium_count = values.str.contains(
                "medium"
            ).sum()

            low_count = values.str.contains(
                "low"
            ).sum()

        else:

            high_count = 0
            medium_count = 0
            low_count = len(risk_df)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "👥 Total Students",
                len(risk_df)
            )

        with c2:
            st.metric(
                "🔴 High Risk",
                high_count
            )

        with c3:
            st.metric(
                "🟠 Medium Risk",
                medium_count
            )

        with c4:
            st.metric(
                "🟢 Low Risk",
                low_count
            )

        st.divider()

        if risk_column:

            selected_risk = st.selectbox(
                "Filter by Risk Level",
                [
                    "All",
                    "High",
                    "Medium",
                    "Low"
                ]
            )

            if selected_risk == "All":

                filtered_df = risk_df

            else:

                filtered_df = risk_df[
                    risk_df[risk_column]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        selected_risk.lower()
                    )
                ]

        else:

            filtered_df = risk_df

        st.markdown("### 📋 Student Data")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        try:

            excel_file = create_excel_file(
                filtered_df
            )

            st.download_button(
                "⬇️ Download Mentor Report",
                data=excel_file,
                file_name="student_risk_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        except Exception:

            csv_data = filtered_df.to_csv(
                index=False
            )

            st.download_button(
                "⬇️ Download Mentor Report",
                data=csv_data,
                file_name="student_risk_report.csv",
                mime="text/csv"
            )

        if risk_column:

            st.markdown(
                "### 📊 Risk Distribution"
            )

            chart_data = (
                risk_df[risk_column]
                .astype(str)
                .value_counts()
            )

            st.bar_chart(
                chart_data
            )


elif page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">📊 Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Project performance and chatbot usage analytics.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "🤖 Campus AI uses retrieval-based NLP with "
        "TF-IDF and cosine similarity to answer "
        "college-related questions."
    )

    st.markdown(
        "### 🧠 Risk Prediction Model"
    )

    model = get_risk_model()

    if model is not None:

        st.success(
            "Risk prediction model loaded successfully."
        )

        if hasattr(
            model,
            "feature_importances_"
        ):

            importance = model.feature_importances_

            feature_names = [
                f"Feature {i + 1}"
                for i in range(
                    len(importance)
                )
            ]

            importance_df = pd.DataFrame(
                {
                    "Feature": feature_names,
                    "Importance": importance
                }
            )

            importance_df = importance_df.sort_values(
                "Importance",
                ascending=False
            )

            st.markdown(
                "#### Feature Importance"
            )

            st.bar_chart(
                importance_df.set_index(
                    "Feature"
                )
            )

    else:

        st.warning(
            "Risk prediction model could not be loaded."
        )

    st.divider()

    st.markdown(
        "### 💬 Chatbot Usage"
    )

    log_path = os.path.join(
        "logs",
        "queries.csv"
    )

    if os.path.exists(log_path):

        try:

            logs_df = pd.read_csv(
                log_path
            )

            st.metric(
                "Total Questions",
                len(logs_df)
            )

            st.dataframe(
                logs_df,
                use_container_width=True,
                hide_index=True
            )

        except Exception:

            st.info(
                "Chatbot log data is not available yet."
            )

    else:

        st.info(
            "No chatbot questions have been logged yet."
        )


elif page == "ℹ️ About":

    st.markdown(
        """<div class="about-title">ℹ️ About Campus AI</div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<div class="about-intro">🎓 <b>Campus AI Assistant</b> is an AI-powered college support platform developed as an <b>AI & Data Science final-year project</b>. It helps students quickly access important college information through a simple conversational interface.</div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<div class="about-section">
<div class="about-heading">📚 Supported Areas</div>
<div class="about-list">
<div>📚 <b>Courses and Departments</b></div>
<div>💰 <b>Fees and Scholarships</b></div>
<div>📝 <b>Admissions</b></div>
<div>📅 <b>Attendance and Examinations</b></div>
<div>🏠 <b>Hostel and Transport</b></div>
<div>💼 <b>Placements</b></div>
<div>🎯 <b>College Information</b></div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<div class="about-section">
<div class="about-heading">🚨 Student Early Warning System</div>
<div class="about-text">The <b>Student Risk Dashboard</b> analyses available student data and helps identify students who may require academic mentoring.</div>
</div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<div class="about-section">
<div class="about-heading">🛠️ Technologies Used</div>
<div class="tech-grid">
<div class="tech-card"><div class="tech-icon">🐍</div><div><div class="tech-name">Programming</div><div class="tech-value">Python</div></div></div>
<div class="tech-card"><div class="tech-icon">🖥️</div><div><div class="tech-name">Frontend</div><div class="tech-value">Streamlit</div></div></div>
<div class="tech-card"><div class="tech-icon">🧠</div><div><div class="tech-name">NLP</div><div class="tech-value">TF-IDF &amp; Cosine Similarity</div></div></div>
<div class="tech-card"><div class="tech-icon">🤖</div><div><div class="tech-name">Machine Learning</div><div class="tech-value">Scikit-learn</div></div></div>
<div class="tech-card"><div class="tech-icon">📊</div><div><div class="tech-name">Data Processing</div><div class="tech-value">Pandas</div></div></div>
<div class="tech-card"><div class="tech-icon">💾</div><div><div class="tech-name">Model Storage</div><div class="tech-value">Joblib</div></div></div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<div class="about-footer"><b>V.S.B Engineering College</b><br>Campus AI Assistant • AI &amp; DS Final Year Project</div>""",
        unsafe_allow_html=True
    )
