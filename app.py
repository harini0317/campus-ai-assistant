import os
import io
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from chatbot import CollegeBot
import risk



st.set_page_config(
    page_title="V.S.B Engineering College | Campus AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Main title */
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #4b5563;
        margin-bottom: 25px;
    }

    /* Cards */
    .card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 22px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .card-text {
        font-size: 15px;
        color: #374151;
        line-height: 1.6;
    }

    /* Chatbot messages */
    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
    }

    /* IMPORTANT: chatbot text visibility */
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong {
        color: #111827 !important;
    }

    [data-testid="stChatMessage"] ul,
    [data-testid="stChatMessage"] ol {
        color: #111827 !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] textarea {
        color: #111827 !important;
        background: #ffffff !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
    }

    /* Normal text */
    .stMarkdown,
    .stText {
        color: #111827;
    }

    /* Metric */
    [data-testid="stMetric"] {
        background: #ffffff;
        padding: 15px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
    }

    [data-testid="stMetricLabel"] {
        color: #4b5563 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 25px;
        margin-top: 40px;
        color: #6b7280;
        font-size: 14px;
        border-top: 1px solid #e5e7eb;
    }

    /* Quick question buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


COLLEGE = "V.S.B Engineering College"


def get_bot():
    return CollegeBot()


@st.cache_resource
def get_risk():
    return risk.load()


def load_sample_data():
    path = os.path.join("data", "sample_class.csv")

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def create_download_file(df):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Risk Report")

    output.seek(0)
    return output



with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:10px;">
            <div style="font-size:45px;">🎓</div>
            <h2 style="margin:0;">Campus AI</h2>
            <p style="color:#d1d5db !important;">
                Smart College Assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

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

    st.markdown(
        """
        <div style="text-align:center; color:#d1d5db;">
            <small>
                V.S.B Engineering College<br>
                AI & DS Final Year Project
            </small>
        </div>
        """,
        unsafe_allow_html=True
    )


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

    # Welcome card
    st.markdown(
        """
        <div class="card">
            <div class="card-title">👋 Vanakkam!</div>
            <div class="card-text">
                Welcome to the V.S.B Engineering College AI Enquiry Assistant.
                <br><br>
                You can ask questions in <b>English or Tanglish</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick questions
    st.markdown("### ⚡ Quick Questions")

    q1, q2, q3, q4 = st.columns(4)

    if "msgs" not in st.session_state:
        st.session_state.msgs = []

    with q1:
        if st.button("📚 Courses", use_container_width=True):
            st.session_state.msgs.append(
                {
                    "role": "user",
                    "content": "VSB la enna courses iruku?"
                }
            )

    with q2:
        if st.button("💰 Fees", use_container_width=True):
            st.session_state.msgs.append(
                {
                    "role": "user",
                    "content": "VSB la fees evlo?"
                }
            )

    with q3:
        if st.button("🏠 Hostel", use_container_width=True):
            st.session_state.msgs.append(
                {
                    "role": "user",
                    "content": "VSB la hostel facility iruka?"
                }
            )

    with q4:
        if st.button("💼 Placements", use_container_width=True):
            st.session_state.msgs.append(
                {
                    "role": "user",
                    "content": "VSB placement la enna companies varanga?"
                }
            )

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.msgs = []
        st.rerun()

    # Display previous messages
    for message in st.session_state.msgs:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

            if "source" in message:
                st.caption(
                    f"📄 Source: {message['source']}  |  "
                    f"Confidence: {message.get('confidence', 'N/A')}"
                )

    # Chat input
    user_question = st.chat_input(
        "Ask V.S.B Engineering College something..."
    )

    if user_question:

        st.session_state.msgs.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        bot = get_bot()

        try:
            result = bot.ask(user_question)

        except Exception:
            try:
                result = bot.get_answer(user_question)
            except Exception as e:
                result = (
                    f"Sorry, chatbot error occurred: {str(e)}"
                )

        # Handle different possible response formats
        answer = ""
        source = ""
        confidence = ""

        if isinstance(result, dict):

            answer = result.get(
                "answer",
                result.get("response", "")
            )

            source = result.get(
                "source",
                result.get("file", "")
            )

            confidence = result.get(
                "confidence",
                ""
            )

        elif isinstance(result, tuple):

            if len(result) >= 1:
                answer = result[0]

            if len(result) >= 2:
                source = result[1]

            if len(result) >= 3:
                confidence = result[2]

        else:
            answer = str(result)

        with st.chat_message("assistant"):

            st.markdown(answer)

            if source or confidence:

                source_text = "📄"

                if source:
                    source_text += f" Source: {source}"

                if confidence:
                    source_text += f" | Confidence: {confidence}"

                st.caption(source_text)

        st.session_state.msgs.append(
            {
                "role": "assistant",
                "content": answer,
                "source": source,
                "confidence": confidence
            }
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

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

    else:

        df = load_sample_data()

        st.info(
            "Showing sample student data. "
            "Upload your own CSV to analyse students."
        )

    if df.empty:

        st.warning("No student data available.")

    else:

        # Try risk model
        risk_df = df.copy()

        try:

            model = get_risk()

            if model is not None:

                # Common prediction formats
                if hasattr(model, "predict"):

                    numeric_df = risk_df.select_dtypes(
                        include=["number"]
                    )

                    if not numeric_df.empty:

                        predictions = model.predict(
                            numeric_df
                        )

                        risk_df["Risk"] = predictions

        except Exception:
            pass

        # Detect existing risk column
        risk_column = None

        for col in risk_df.columns:

            if col.lower() in [
                "risk",
                "risk_level",
                "risk level"
            ]:
                risk_column = col
                break

        if risk_column is not None:

            risk_values = (
                risk_df[risk_column]
                .astype(str)
                .str.lower()
            )

            high_count = risk_values.str.contains(
                "high"
            ).sum()

            medium_count = risk_values.str.contains(
                "medium"
            ).sum()

            low_count = risk_values.str.contains(
                "low"
            ).sum()

        else:

            high_count = 0
            medium_count = 0
            low_count = len(risk_df)

        # Metrics
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

        # Filter
        if risk_column:

            risk_options = [
                "All",
                "High",
                "Medium",
                "Low"
            ]

            selected_risk = st.selectbox(
                "Filter by Risk Level",
                risk_options
            )

            if selected_risk != "All":

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

        else:

            filtered_df = risk_df

        st.markdown("### 📋 Student Data")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        # Download
        try:

            excel_file = create_download_file(
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

        # Risk chart
        if risk_column:

            st.markdown("### 📊 Risk Distribution")

            chart_data = (
                risk_df[risk_column]
                .astype(str)
                .value_counts()
            )

            st.bar_chart(chart_data)




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

    # Model comparison
    st.markdown(
        """
        <div class="card">
            <div class="card-title">🤖 AI Model</div>
            <div class="card-text">
                Campus AI uses machine learning and retrieval-based
                techniques to support college enquiries and identify
                students who may need academic attention.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Risk Prediction")

    try:

        model = get_risk()

        if model is not None:

            st.success(
                "Risk prediction model loaded successfully."
            )

            if hasattr(model, "feature_importances_"):

                importance = model.feature_importances_

                st.markdown(
                    "#### Feature Importance"
                )

                feature_names = [
                    f"Feature {i + 1}"
                    for i in range(len(importance))
                ]

                importance_df = pd.DataFrame(
                    {
                        "Feature": feature_names,
                        "Importance": importance
                    }
                ).sort_values(
                    "Importance",
                    ascending=False
                )

                st.bar_chart(
                    importance_df.set_index(
                        "Feature"
                    )
                )

        else:

            st.warning(
                "Risk model could not be loaded."
            )

    except Exception as e:

        st.warning(
            f"Risk model information unavailable: {e}"
        )

    st.divider()

    # Chatbot logs
    st.markdown("### 💬 Chatbot Usage")

    log_path = os.path.join(
        "logs",
        "queries.csv"
    )

    if os.path.exists(log_path):

        try:

            logs_df = pd.read_csv(log_path)

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
        '<div class="main-title">ℹ️ About Campus AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                🎓 Campus AI Assistant
            </div>

            <div class="card-text">

                <b>Campus AI Assistant</b> is an AI-powered
                college support platform developed as an
                AI & Data Science final-year project.

                <br><br>

                The system provides a college enquiry chatbot
                that can answer questions about:

                <ul>
                    <li>📚 Courses and Departments</li>
                    <li>💰 Fees and Scholarships</li>
                    <li>📝 Admissions</li>
                    <li>📅 Attendance and Examinations</li>
                    <li>🏠 Hostel and Transport</li>
                    <li>💼 Placements</li>
                    <li>🎯 College Events</li>
                </ul>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                🚨 Student Early Warning System
            </div>

            <div class="card-text">

                The project also includes a student risk
                dashboard that can help identify students
                who may require academic mentoring.

                Student information can be analysed using
                attendance, academic and other available
                features.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                🧠 Technologies
            </div>

            <div class="card-text">

                <b>Frontend:</b> Streamlit<br>
                <b>Programming:</b> Python<br>
                <b>AI:</b> TF-IDF / Retrieval-Based NLP<br>
                <b>Machine Learning:</b> Scikit-learn<br>
                <b>Data:</b> Pandas<br>
                <b>Model Storage:</b> Joblib

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )




st.markdown(
    """
    <div class="footer">
        V.S.B Engineering College • Campus AI Assistant<br>
        AI & DS Final Year Project
    </div>
    """,
    unsafe_allow_html=True
)