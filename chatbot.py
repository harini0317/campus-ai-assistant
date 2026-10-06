import os
import re
import csv
from datetime import datetime

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)


class CollegeBot:

    def __init__(self):
        self.files = {
            "admissions": os.path.join(KB_DIR, "admissions.txt"),
            "fees": os.path.join(KB_DIR, "fees.txt"),
            "exams": os.path.join(KB_DIR, "exams_attendance.txt"),
            "hostel": os.path.join(KB_DIR, "hostel_transport.txt"),
            "placements": os.path.join(KB_DIR, "placements_events.txt"),
        }

        self.documents = []
        self.sources = []

        self._load_knowledge_base()

        if self.documents:
            self.vectorizer = TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                stop_words="english"
            )

            self.matrix = self.vectorizer.fit_transform(self.documents)
        else:
            self.vectorizer = None
            self.matrix = None

    # ---------------------------------------------------------
    # LOAD KNOWLEDGE BASE
    # ---------------------------------------------------------

    def _load_knowledge_base(self):

        for source, file_path in self.files.items():

            if not os.path.exists(file_path):
                continue

            try:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()

                chunks = self._make_chunks(text)

                for chunk in chunks:
                    self.documents.append(chunk)
                    self.sources.append(source)

            except Exception:
                continue

    # ---------------------------------------------------------
    # SPLIT DOCUMENT INTO CHUNKS
    # ---------------------------------------------------------

    def _make_chunks(self, text):

        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", text)
            if p.strip()
        ]

        return paragraphs

    # ---------------------------------------------------------
    # NORMALIZE USER QUESTION
    # ---------------------------------------------------------

    def _norm(self, text):

        text = text.lower().strip()

        replacements = {
            "courses": "course",
            "programs": "program",
            "departments": "department",
            "fees": "fee",
            "admissions": "admission",
            "placements": "placement",
            "hostels": "hostel",
            "attendance": "attendance",
            "evlo": "how many",
            "ethana": "how many",
            "enna": "what",
            "iruku": "is there",
            "irukka": "is there",
            "epdi": "how",
        }

        for old, new in replacements.items():
            text = re.sub(
                rf"\b{re.escape(old)}\b",
                new,
                text
            )

        return text

    # ---------------------------------------------------------
    # COURSE COUNT QUESTION
    # ---------------------------------------------------------

    def _is_course_count_question(self, question):

        q = question.lower().strip()

        patterns = [
            r"how many course",
            r"how many courses",
            r"how many program",
            r"how many programs",
            r"how many department",
            r"how many departments",
            r"number of course",
            r"number of courses",
            r"number of program",
            r"number of programs",
            r"number of department",
            r"number of departments",
            r"total course",
            r"total courses",
            r"total program",
            r"total programs",
            r"total department",
            r"total departments",
            r"evlo course",
            r"evlo courses",
            r"evlo program",
            r"evlo programs",
            r"evlo department",
            r"evlo departments",
            r"ethana course",
            r"ethana courses",
            r"ethana program",
            r"ethana programs",
            r"how much course",
        ]

        return any(re.search(pattern, q) for pattern in patterns)

    def _get_course_count_answer(self):

        return (
            "V.S.B Engineering College currently offers 12 undergraduate "
            "engineering programs."
        )

    # ---------------------------------------------------------
    # ADMISSION PROCESS QUESTION
    # ---------------------------------------------------------

    def _is_admission_process_question(self, question):

        q = question.lower().strip()

        patterns = [
            "admission process",
            "admission procedure",
            "admission steps",
            "how to apply",
            "how can i apply",
            "how to get admission",
            "how do i get admission",
            "admission epdi",
            "admission ena",
            "admission eppadi",
            "admission apply",
            "apply admission",
        ]

        return any(pattern in q for pattern in patterns)

    def _get_admission_process_answer(self):

        return """The admission process at V.S.B Engineering College is:

1. Online Registration
2. Application Fee Payment – ₹100 (non-refundable)
3. Seat Confirmation
4. Document Upload
5. Counseling
6. Document Verification

For the latest admission information, students should confirm the current details with the college."""

    # ---------------------------------------------------------
    # COURSE LIST QUESTION
    # ---------------------------------------------------------

    def _is_course_question(self, question):

        q = question.lower().strip()

        patterns = [
            "what courses",
            "what course",
            "which courses",
            "which course",
            "courses offered",
            "course offered",
            "programs offered",
            "program offered",
            "departments",
            "department",
            "course list",
            "program list",
            "enna course",
            "enna courses",
            "enna program",
            "enna programs",
            "vsb la enna course",
            "vsb la enna courses",
            "vsb college courses",
            "college courses",
        ]

        return any(pattern in q for pattern in patterns)

    def _get_course_answer(self):

        answer = (
            "V.S.B Engineering College offers the following "
            "undergraduate engineering programs:\n\n"
            "1. B.Tech Artificial Intelligence and Data Science\n"
            "2. B.Tech Biotechnology\n"
            "3. B.Tech Chemical Engineering\n"
            "4. B.E Civil Engineering\n"
            "5. B.Tech Computer Science and Business System\n"
            "6. B.E Computer and Communication Engineering\n"
            "7. B.E Computer Science and Engineering\n"
            "8. B.E Computer Science and Engineering (AI & ML)\n"
            "9. B.E Electronics and Communication Engineering\n"
            "10. B.E Electrical and Electronics Engineering\n"
            "11. B.Tech Information Technology\n"
            "12. Mechanical Engineering"
        )

        # Remove Biomedical Engineering if it still exists
        # in an older admissions.txt file.
        answer = re.sub(
            r"\n*The college website also lists Biomedical Engineering "
            r"among its undergraduate programs\.?",
            "",
            answer,
            flags=re.IGNORECASE
        )

        answer = re.sub(
            r"\n*Biomedical Engineering\.?",
            "",
            answer,
            flags=re.IGNORECASE
        )

        return answer.strip()

    # ---------------------------------------------------------
    # CATEGORY DETECTION
    # ---------------------------------------------------------

    def _detect_category(self, question):

        q = question.lower()

        if any(word in q for word in [
            "fee",
            "fees",
            "tuition",
            "scholarship",
            "cutoff",
            "cut off"
        ]):
            return "fees"

        if any(word in q for word in [
            "attendance",
            "exam",
            "exams",
            "internal",
            "semester",
            "coe",
            "mark",
            "marks",
            "result",
            "test"
        ]):
            return "exams"

        if any(word in q for word in [
            "hostel",
            "bus",
            "transport",
            "mess",
            "outing"
        ]):
            return "hostel"

        if any(word in q for word in [
            "placement",
            "placements",
            "job",
            "jobs",
            "company",
            "companies",
            "internship",
            "event"
        ]):
            return "placements"

        if any(word in q for word in [
            "admission",
            "admissions",
            "apply",
            "eligibility",
            "eligible",
            "quota",
            "college address",
            "address",
            "contact",
            "phone",
            "email"
        ]):
            return "admissions"

        return None

    # ---------------------------------------------------------
    # SEARCH KNOWLEDGE BASE
    # ---------------------------------------------------------

    def _search(self, question):

        if self.vectorizer is None or self.matrix is None:
            return None, None, 0.0

        try:

            query_vector = self.vectorizer.transform([question])

            similarities = cosine_similarity(
                query_vector,
                self.matrix
            )[0]

            best_index = int(np.argmax(similarities))
            score = float(similarities[best_index])

            if score <= 0:
                return None, None, 0.0

            answer = self.documents[best_index]
            source = self.sources[best_index]

            return answer, source, score

        except Exception:
            return None, None, 0.0

    # ---------------------------------------------------------
    # CLEAN ANSWER
    # ---------------------------------------------------------

    def _clean_answer(self, answer):

        if not answer:
            return answer

        answer = re.sub(
            r"\n*The college website also lists Biomedical Engineering "
            r"among its undergraduate programs\.?",
            "",
            answer,
            flags=re.IGNORECASE
        )

        answer = re.sub(
            r"\n*Biomedical Engineering\.?",
            "",
            answer,
            flags=re.IGNORECASE
        )

        return answer.strip()

    # ---------------------------------------------------------
    # LOG QUERY
    # ---------------------------------------------------------

    def _log(self, question, score, source):

        log_file = os.path.join(
            LOG_DIR,
            "queries.csv"
        )

        file_exists = os.path.exists(log_file)

        try:

            with open(
                log_file,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow([
                        "timestamp",
                        "question",
                        "score",
                        "source"
                    ])

                writer.writerow([
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    question,
                    round(score, 3),
                    source
                ])

        except Exception:
            pass

    # ---------------------------------------------------------
    # MAIN ASK FUNCTION
    # ---------------------------------------------------------

    def ask(self, question):

        if not question or not question.strip():

            return {
                "answer": "Please enter a question.",
                "confidence": 0.0,
                "hits": []
            }

        question = question.strip()

        # ---------------------------------------------
        # COURSE COUNT
        # ---------------------------------------------

        if self._is_course_count_question(question):

            answer = self._get_course_count_answer()

            self._log(
                question,
                1.0,
                "admissions.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "admissions.txt",
                        1.0
                    )
                ]
            }

        # ---------------------------------------------
        # ADMISSION PROCESS
        # ---------------------------------------------

        if self._is_admission_process_question(question):

            answer = self._get_admission_process_answer()

            self._log(
                question,
                1.0,
                "admissions.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "admissions.txt",
                        1.0
                    )
                ]
            }

        # ---------------------------------------------
        # COURSE LIST
        # ---------------------------------------------

        if self._is_course_question(question):

            answer = self._get_course_answer()

            self._log(
                question,
                1.0,
                "admissions.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "admissions.txt",
                        1.0
                    )
                ]
            }

        # ---------------------------------------------
        # CATEGORY BASED SEARCH
        # ---------------------------------------------

        category = self._detect_category(question)

        if category:

            category_file = self.files.get(category)

            if category_file and os.path.exists(category_file):

                try:

                    with open(
                        category_file,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        text = file.read()

                    chunks = self._make_chunks(text)

                    if chunks:

                        local_vectorizer = TfidfVectorizer(
                            lowercase=True,
                            ngram_range=(1, 2),
                            stop_words="english"
                        )

                        local_matrix = (
                            local_vectorizer.fit_transform(chunks)
                        )

                        query_vector = (
                            local_vectorizer.transform([question])
                        )

                        similarities = cosine_similarity(
                            query_vector,
                            local_matrix
                        )[0]

                        best_index = int(
                            np.argmax(similarities)
                        )

                        score = float(
                            similarities[best_index]
                        )

                        answer = self._clean_answer(
                            chunks[best_index]
                        )

                        source = os.path.basename(
                            category_file
                        )

                        if score > 0:

                            self._log(
                                question,
                                score,
                                source
                            )

                            return {
                                "answer": answer,
                                "confidence": round(
                                    score,
                                    3
                                ),
                                "hits": [
                                    (
                                        answer,
                                        source,
                                        score
                                    )
                                ]
                            }

                except Exception:
                    pass

        # ---------------------------------------------
        # GENERAL TF-IDF SEARCH
        # ---------------------------------------------

        answer, source, score = self._search(
            question
        )

        if answer:

            answer = self._clean_answer(answer)

            source_file = (
                f"{source}.txt"
                if source in self.files
                else source
            )

            self._log(
                question,
                score,
                source_file
            )

            return {
                "answer": answer,
                "confidence": round(score, 3),
                "hits": [
                    (
                        answer,
                        source_file,
                        score
                    )
                ]
            }

        # ---------------------------------------------
        # FALLBACK
        # ---------------------------------------------

        fallback = (
            "Sorry, I could not find a clear answer for that question. "
            "Please try asking about admissions, courses, fees, hostel, "
            "attendance, exams, placements or internships."
        )

        self._log(
            question,
            0.0,
            "No matching source"
        )

        return {
            "answer": fallback,
            "confidence": 0.0,
            "hits": []
        }

    # ---------------------------------------------------------
    # GET ANSWER
    # ---------------------------------------------------------

    def get_answer(self, question):

        return self.ask(question)
