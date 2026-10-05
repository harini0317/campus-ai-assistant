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


class CollegeBot:

    def __init__(self):

        self.files = {
            "admissions": "admissions.txt",
            "fees": "fees.txt",
            "exams": "exams_attendance.txt",
            "hostel": "hostel_transport.txt",
            "placements": "placements_events.txt",
        }

        self.documents = {}
        self.vectorizers = {}
        self.matrices = {}

        self._load_documents()

    # -----------------------------------------------------
    # LOAD KNOWLEDGE BASE
    # -----------------------------------------------------

    def _load_documents(self):

        for key, filename in self.files.items():

            path = os.path.join(KB_DIR, filename)

            if not os.path.exists(path):
                self.documents[key] = []
                continue

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                text = f.read()

            chunks = self._make_chunks(text)

            self.documents[key] = chunks

            if chunks:

                vectorizer = TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 2),
                    sublinear_tf=True
                )

                matrix = vectorizer.fit_transform(chunks)

                self.vectorizers[key] = vectorizer
                self.matrices[key] = matrix

    # -----------------------------------------------------
    # TEXT NORMALIZATION
    # -----------------------------------------------------

    def _norm(self, text):

        text = text.lower()

        replacements = {
            "fees": "fee",
            "fee": "fee",
            "fess": "fee",
            "feess": "fee",

            "attendance": "attendance",
            "attendence": "attendance",

            "hostel": "hostel",
            "hostal": "hostel",

            "placement": "placement",
            "placements": "placement",

            "admission": "admission",
            "admissions": "admission",

            "course": "course",
            "courses": "course",

            "exam": "exam",
            "exams": "exam",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return re.sub(r"\s+", " ", text).strip()

    # -----------------------------------------------------
    # SPLIT DOCUMENT INTO USEFUL SECTIONS
    # -----------------------------------------------------

    def _make_chunks(self, text):

        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", text)
            if p.strip()
        ]

        return paragraphs

    # -----------------------------------------------------
    # CATEGORY DETECTION
    # -----------------------------------------------------

    def _get_category(self, question):

        q = self._norm(question)

        # ATTENDANCE / EXAM FIRST
        attendance_words = [
            "attendance",
            "attend",
            "absent",
            "percentage attendance",
            "exam eligibility",
            "semester exam",
            "end semester",
            "internal exam",
            "unit test",
            "model exam",
            "retest",
            "coe",
            "hall ticket"
        ]

        if any(word in q for word in attendance_words):
            return "exams"

        # FEES
        fee_words = [
            "fee",
            "fees",
            "tuition",
            "payment",
            "cost",
            "amount",
            "how much",
            "evlo",
            "panam"
        ]

        if any(word in q for word in fee_words):
            return "fees"

        # HOSTEL / TRANSPORT
        hostel_words = [
            "hostel",
            "hostal",
            "mess",
            "room",
            "boys hostel",
            "girls hostel",
            "transport",
            "bus",
            "college bus",
            "route"
        ]

        if any(word in q for word in hostel_words):
            return "hostel"

        # PLACEMENT / EVENTS
        placement_words = [
            "placement",
            "placements",
            "company",
            "companies",
            "job",
            "jobs",
            "salary",
            "package",
            "lpa",
            "recruitment",
            "career",
            "internship",
            "event",
            "events",
            "workshop",
            "seminar",
            "training"
        ]

        if any(word in q for word in placement_words):
            return "placements"

        # COURSES / ADMISSION
        admission_words = [
            "course",
            "courses",
            "program",
            "programs",
            "department",
            "departments",
            "branch",
            "branches",
            "degree",
            "degrees",
            "admission",
            "admissions",
            "eligibility",
            "apply",
            "application",
            "counselling",
            "counseling",
            "lateral entry",
            "quota",
            "scholarship",
            "scholarships",
            "cutoff",
            "cut off"
        ]

        if any(word in q for word in admission_words):
            return "admissions"

        return None

    # -----------------------------------------------------
    # COURSE QUESTION
    # -----------------------------------------------------

    def _is_course_question(self, question):

        q = self._norm(question)

        patterns = [
            "what course",
            "which course",
            "list course",
            "course available",
            "course offer",
            "enna course",
            "enna courses",
            "entha course",
            "entha courses",
            "which branch",
            "enna branch",
            "branches available",
            "departments available",
            "what departments",
            "program available",
            "enna program",
            "which program",
            "degree available"
        ]

        return any(p in q for p in patterns)

    # -----------------------------------------------------
    # FULL COURSE ANSWER
    # -----------------------------------------------------

    def _get_course_answer(self):

        chunks = self.documents.get("admissions", [])

        for i, chunk in enumerate(chunks):

            if "undergraduate engineering programs" in chunk.lower():

                answer = chunk

                # Add next useful paragraph if needed
                for next_chunk in chunks[i + 1:i + 3]:

                    if (
                        "admission process" not in next_chunk.lower()
                        and "eligibility" not in next_chunk.lower()
                    ):
                        answer += "\n\n" + next_chunk

                return answer

        return None

    # -----------------------------------------------------
    # FULL FEE ANSWER
    # -----------------------------------------------------

    def _get_fee_answer(self):

        chunks = self.documents.get("fees", [])

        selected = []

        keywords = [
            "fee structure",
            "government quota",
            "management quota",
            "accredited",
            "non-accredited",
            "scholarship",
            "tuition fee",
            "₹"
        ]

        for chunk in chunks:

            low = chunk.lower()

            if any(word.lower() in low for word in keywords):
                selected.append(chunk)

        if selected:

            # Remove duplicate chunks
            unique = []

            for chunk in selected:
                if chunk not in unique:
                    unique.append(chunk)

            return "\n\n".join(unique)

        return "\n\n".join(chunks)

    # -----------------------------------------------------
    # FULL ATTENDANCE / EXAM ANSWER
    # -----------------------------------------------------

    def _get_exam_answer(self, question):

        chunks = self.documents.get("exams", [])

        q = self._norm(question)

        selected = []

        if "attendance" in q or "attend" in q:

            keywords = [
                "attendance",
                "75%",
                "65%",
                "75",
                "65",
                "end-semester",
                "semester"
            ]

            for chunk in chunks:

                if any(
                    word.lower() in chunk.lower()
                    for word in keywords
                ):
                    selected.append(chunk)

        else:

            keywords = [
                "exam",
                "internal",
                "unit test",
                "model",
                "retest",
                "coe"
            ]

            for chunk in chunks:

                if any(
                    word.lower() in chunk.lower()
                    for word in keywords
                ):
                    selected.append(chunk)

        if selected:

            unique = []

            for chunk in selected:
                if chunk not in unique:
                    unique.append(chunk)

            return "\n\n".join(unique)

        return "\n\n".join(chunks)

    # -----------------------------------------------------
    # FULL HOSTEL ANSWER
    # -----------------------------------------------------

    def _get_hostel_answer(self):

        chunks = self.documents.get("hostel", [])

        return "\n\n".join(chunks)

    # -----------------------------------------------------
    # FULL PLACEMENT ANSWER
    # -----------------------------------------------------

    def _get_placement_answer(self):

        chunks = self.documents.get("placements", [])

        return "\n\n".join(chunks)

    # -----------------------------------------------------
    # LOG QUESTIONS
    # -----------------------------------------------------

    def _log(self, question, source, confidence):

        os.makedirs(LOG_DIR, exist_ok=True)

        path = os.path.join(
            LOG_DIR,
            "queries.csv"
        )

        exists = os.path.exists(path)

        with open(
            path,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            if not exists:
                writer.writerow(
                    [
                        "timestamp",
                        "question",
                        "source",
                        "confidence"
                    ]
                )

            writer.writerow(
                [
                    datetime.now().isoformat(),
                    question,
                    source,
                    confidence
                ]
            )

    # -----------------------------------------------------
    # MAIN ASK FUNCTION
    # -----------------------------------------------------

    def ask(self, question):

        question = question.strip()

        if not question:

            return {
                "answer": "Please ask a question.",
                "confidence": 0,
                "hits": []
            }

        category = self._get_category(question)

        # -------------------------------------------------
        # COURSES
        # -------------------------------------------------

        if self._is_course_question(question):

            answer = self._get_course_answer()

            if answer:

                source = "admissions.txt"

                self._log(
                    question,
                    source,
                    1.0
                )

                return {
                    "answer": answer,
                    "confidence": 1.0,
                    "hits": [
                        (answer, source, 1.0)
                    ]
                }

        # -------------------------------------------------
        # FEES
        # -------------------------------------------------

        if category == "fees":

            answer = self._get_fee_answer()

            source = "fees.txt"

            self._log(
                question,
                source,
                1.0
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (answer, source, 1.0)
                ]
            }

        # -------------------------------------------------
        # ATTENDANCE / EXAMS
        # -------------------------------------------------

        if category == "exams":

            answer = self._get_exam_answer(question)

            source = "exams_attendance.txt"

            self._log(
                question,
                source,
                1.0
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (answer, source, 1.0)
                ]
            }

        # -------------------------------------------------
        # HOSTEL
        # -------------------------------------------------

        if category == "hostel":

            answer = self._get_hostel_answer()

            source = "hostel_transport.txt"

            self._log(
                question,
                source,
                1.0
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (answer, source, 1.0)
                ]
            }

        # -------------------------------------------------
        # PLACEMENTS
        # -------------------------------------------------

        if category == "placements":

            answer = self._get_placement_answer()

            source = "placements_events.txt"

            self._log(
                question,
                source,
                1.0
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (answer, source, 1.0)
                ]
            }

        # -------------------------------------------------
        # ADMISSIONS
        # -------------------------------------------------

        if category == "admissions":

            chunks = self.documents.get("admissions", [])

            if chunks:

                answer = "\n\n".join(chunks)

                source = "admissions.txt"

                self._log(
                    question,
                    source,
                    1.0
                )

                return {
                    "answer": answer,
                    "confidence": 1.0,
                    "hits": [
                        (answer, source, 1.0)
                    ]
                }

        # -------------------------------------------------
        # GENERAL TF-IDF FALLBACK
        # -------------------------------------------------

        best_chunk = None
        best_source = None
        best_score = 0.0

        for key, chunks in self.documents.items():

            if not chunks:
                continue

            vectorizer = self.vectorizers.get(key)
            matrix = self.matrices.get(key)

            if vectorizer is None or matrix is None:
                continue

            try:

                q_vector = vectorizer.transform(
                    [question]
                )

                scores = cosine_similarity(
                    q_vector,
                    matrix
                )[0]

                index = int(
                    np.argmax(scores)
                )

                score = float(
                    scores[index]
                )

                if score > best_score:

                    best_score = score
                    best_chunk = chunks[index]
                    best_source = self.files[key]

            except Exception:
                continue

        if best_chunk is None or best_score < 0.15:

            answer = (
                "Sorry, I couldn't find a reliable answer "
                "for that question in the college knowledge base."
            )

            self._log(
                question,
                "none",
                best_score
            )

            return {
                "answer": answer,
                "confidence": best_score,
                "hits": []
            }

        self._log(
            question,
            best_source,
            best_score
        )

        return {
            "answer": best_chunk,
            "confidence": best_score,
            "hits": [
                (best_chunk, best_source, best_score)
            ]
        }
        