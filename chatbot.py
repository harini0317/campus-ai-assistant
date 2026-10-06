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

    def _load_knowledge_base(self):
        for source, file_path in self.files.items():
            if not os.path.exists(file_path):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()

                chunks = self._make_chunks(text)

                for chunk in chunks:
                    self.documents.append(chunk)
                    self.sources.append(source)

            except Exception:
                continue

    def _make_chunks(self, text):
        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", text)
            if p.strip()
        ]

        chunks = []

        for paragraph in paragraphs:
            if len(paragraph.split()) >= 8:
                chunks.append(paragraph)

        return chunks

    def _norm(self, text):
        text = text.lower().strip()

        replacements = {
            "courses": "course",
            "programs": "program",
            "departments": "department",
            "fees": "fee",
            "fess": "fee",
            "feee": "fee",
            "feees": "fee",
            "admissions": "admission",
            "placements": "placement",
            "hostels": "hostel",
            "evlo": "how many",
            "ethana": "how many",
            "enna": "what",
            "iruku": "is there",
            "irukka": "is there",
            "epdi": "how",
            "eppadi": "how",
        }

        for old, new in replacements.items():
            text = re.sub(
                rf"\b{re.escape(old)}\b",
                new,
                text
            )

        return text

    def _is_course_count_question(self, question):
        q = self._norm(question)
        q = re.sub(r"\s+", " ", q).strip()

        patterns = [
            "how many course",
            "how many program",
            "how many department",
            "number of course",
            "number of program",
            "number of department",
            "total course",
            "total program",
            "total department",
            "how many course are there",
            "how many program are there",
            "how many department are there",
            "course how many",
            "program how many",
            "department how many",
            "course how many are there",
            "program how many are there",
            "department how many are there",
            "course evlo",
            "courses evlo",
            "course ethana",
            "courses ethana",
            "ethana course",
            "ethana courses",
            "evlo course",
            "evlo courses",
            "course how much",
            "courses how much",
            "how many course in vsb",
            "how many program in vsb",
            "course in vsb how many",
            "courses in vsb how many",
            "vsb course how many",
            "vsb courses how many",
        ]

        if any(pattern in q for pattern in patterns):
            return True

        has_academic_item = any(
            word in q
            for word in [
                "course",
                "program",
                "department"
            ]
        )

        asks_quantity = any(
            phrase in q
            for phrase in [
                "how many",
                "number of",
                "total"
            ]
        )

        return has_academic_item and asks_quantity

    def _get_course_count_answer(self):
        return (
            "V.S.B Engineering College currently offers "
            "12 undergraduate engineering programs."
        )

    def _is_fee_question(self, question):
        q = self._norm(question)
        q = re.sub(r"\s+", " ", q).strip()

        fee_words = [
            "fee",
            "tuition",
            "college fee",
            "college fees",
            "course fee",
            "course fees",
            "yearly fee",
            "yearly fees",
            "annual fee",
            "annual fees",
            "fee details",
            "fee structure",
            "fees details",
            "fees structure",
        ]

        return any(word in q for word in fee_words)

    def _get_fee_answer(self):
        return """V.S.B Engineering College UG tuition fees:

• Government Quota – Accredited: ₹55,000 per year

• Government Quota – Non-Accredited: ₹50,000 per year

• Management Quota – Accredited: ₹87,500 per year

• Management Quota – Non-Accredited: ₹85,000 per year

PG fees:

• Accredited: ₹30,000 per semester

• Non-Accredited: ₹25,000 per semester

Merit-based scholarships are also available based on eligibility.

For the latest fee details, students should confirm with the college."""

    def _is_admission_process_question(self, question):
        q = self._norm(question)

        patterns = [
            "admission process",
            "admission procedure",
            "admission steps",
            "how to apply",
            "how can i apply",
            "how to get admission",
            "how do i get admission",
            "admission how",
            "admission apply",
            "apply admission",
            "admission epdi",
            "admission eppadi",
            "admission ena",
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

    def _is_admission_eligibility_question(self, question):
        q = self._norm(question)

        patterns = [
            "admission eligibility",
            "admission eligible",
            "eligibility for admission",
            "eligibility criteria",
            "eligible for admission",
            "who is eligible",
            "admission qualification",
            "qualification for admission",
            "admission requirement",
            "admission requirements",
            "minimum marks for admission",
            "minimum percentage for admission",
            "admission cutoff",
            "admission cut off",
            "hsc eligibility",
            "hsc qualification",
            "admission enna eligibility",
            "admission eligibility enna",
            "eligible ah",
        ]

        return any(pattern in q for pattern in patterns)

    def _get_admission_eligibility_answer(self):
        return """For undergraduate engineering admission at V.S.B Engineering College:

• HSC / 12th pass is required.

• General Category – Minimum 45% average in Mathematics, Physics and Chemistry.

• BC / BCM / MBC / DNC / SC / SCA / ST – Minimum 40% average in Mathematics, Physics and Chemistry.

• HSC Vocational candidates have the applicable eligibility requirements under the admission norms.

Admission is subject to the current State Government / TNEA rules and applicable reservation norms.

Students should confirm the latest eligibility requirements with the college admission office."""

    def _is_course_question(self, question):
        q = self._norm(question)

        patterns = [
            "what course",
            "which course",
            "courses offered",
            "course offered",
            "program offered",
            "programs offered",
            "course list",
            "program list",
            "department",
            "departments",
            "what program",
            "which program",
            "enna course",
            "enna program",
            "vsb la enna course",
            "vsb la enna courses",
            "vsb college course",
            "vsb college courses",
            "college course",
            "college courses",
            "course in vsb",
            "courses in vsb",
        ]

        return any(pattern in q for pattern in patterns)

    def _get_course_answer(self):
        return """V.S.B Engineering College offers the following 12 undergraduate engineering programs:

1. B.Tech Artificial Intelligence and Data Science

2. B.Tech Biotechnology

3. B.Tech Chemical Engineering

4. B.E Civil Engineering

5. B.Tech Computer Science and Business System

6. B.E Computer and Communication Engineering

7. B.E Computer Science and Engineering

8. B.E Computer Science and Engineering (AI & ML)

9. B.E Electronics and Communication Engineering

10. B.E Electrical and Electronics Engineering

11. B.Tech Information Technology

12. B.E Mechanical Engineering"""

    def _is_hostel_question(self, question):
        q = self._norm(question)

        patterns = [
            "hostel",
            "hostel is there",
            "hostel available",
            "hostel facility",
            "hostel facilities",
            "boys hostel",
            "girls hostel",
            "hostel fee",
            "hostel fees",
            "mess",
            "hostel mess",
            "bus facility",
            "college bus",
            "transport",
        ]

        return any(pattern in q for pattern in patterns)

    def _get_hostel_answer(self):
        return """Yes, V.S.B Engineering College provides hostel facilities for both boys and girls.

Hostel facilities include:

• Separate hostel facilities for boys and girls

• Residential accommodation

• Mess facilities

• Basic supporting amenities

• Transport facilities are also available

Hostel fees, room availability and bus fees may vary. Students should confirm the latest details with the college administration."""

    def _is_internship_question(self, question):
        q = self._norm(question)

        patterns = [
            "internship",
            "internships",
            "internship opportunity",
            "internship opportunities",
            "internship available",
            "internships available",
            "internship facility",
            "internship facilities",
            "internship support",
            "internship training",
            "internship company",
            "internship companies",
            "internship program",
            "internship programs",
            "internship chance",
            "internship chances",
            "internship iruka",
            "internship iruku",
            "internship opportunity iruka",
            "internship opportunities iruka",
            "internship available ah",
        ]

        return any(pattern in q for pattern in patterns)

    def _get_internship_answer(self):
        return """V.S.B Engineering College supports students through its Career Development Center (CDC) and career development activities.

Internship-related support may include:

• Career guidance and development activities

• Industry interaction and career-oriented training

• Support for students preparing for internships and placements

• Opportunities connected with industry and professional development

B.Tech students also have a mandatory 6-month internship as part of the academic program.

Students should contact the Career Development Center or respective department for the latest internship opportunities, companies and application details."""

    def _is_placement_question(self, question):
        q = self._norm(question)

        patterns = [
            "placement",
            "placements",
            "placement how",
            "placements how",
            "placement details",
            "placement information",
            "job",
            "jobs",
            "company",
            "companies",
            "salary",
            "package",
            "packages",
            "ctc",
            "placement training",
        ]

        return any(pattern in q for pattern in patterns)

    def _get_placement_answer(self):
        return """V.S.B Engineering College has a Career Development Center (CDC) that supports students with placement training and career development.

According to the current placement information:

• 1177 placement offers are reported

• TCS – 186 offers

• Capgemini – 165 offers

• Cognizant – 30 offers

• Mphasis – 72 offers

• Infosys – 32 offers

• Zoho – 1 offer

• EPAM – 4 offers

The 2024–25 average CTC is listed as ₹7.5 LPA.

The college also provides placement training and career development activities for students.

Students should confirm the latest company-wise opportunities and packages with the Career Development Center."""

    def _is_attendance_question(self, question):
        q = self._norm(question)

        attendance_patterns = [
            "attendance",
            "attendance how many",
            "attendance how",
            "attendance requirement",
            "attendance requirements",
            "attendance percentage",
            "attendance percent",
            "minimum attendance",
            "minimum attendance percentage",
            "how much attendance",
            "how many attendance",
            "attendance needed",
            "attendance required",
            "attendance evlo",
            "attendance ethana",
        ]

        return any(
            pattern in q
            for pattern in attendance_patterns
        )

    def _get_attendance_answer(self):
        return """Students must maintain at least 75% attendance.

• 75% or above – Eligible based on attendance requirement

• 65% to below 75% – May be permitted in eligible cases

• Below 65% – Not permitted to appear for the examinations

Students should confirm any attendance exemption or condonation rules with the college."""

    def _is_exam_question(self, question):
        q = self._norm(question)

        exam_patterns = [
            "exam",
            "examination",
            "exam details",
            "examination details",
            "exam information",
            "examination information",
            "exam process",
            "examination process",
            "exam procedure",
            "examination procedure",
            "exam timetable",
            "examination timetable",
            "exam schedule",
            "examination schedule",
            "internal exam",
            "internal exams",
            "internal test",
            "internal tests",
            "semester exam",
            "semester exams",
            "end semester exam",
            "end semester exams",
            "end semester examination",
            "cia",
            "continuous internal assessment",
            "result",
            "results",
            "grade sheet",
        ]

        return any(
            pattern in q
            for pattern in exam_patterns
        )

    def _get_exam_answer(self):
        return """The examination section at V.S.B Engineering College handles:

• Preparing examination timetables

• Exam hall arrangements

• Invigilator arrangements

• Conducting Continuous Internal Assessment (CIA) Tests

• Conducting End-Semester Examinations

• Processing and publishing examination results

• Issuing grade sheets and examination certificates

Students should check the official college communication for the latest examination timetable and schedule."""

    def _detect_category(self, question):
        q = self._norm(question)

        if any(
            word in q
            for word in [
                "fee",
                "tuition",
                "scholarship",
                "cutoff",
                "cut off"
            ]
        ):
            return "fees"

        if any(
            word in q
            for word in [
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
            ]
        ):
            return "exams"

        if any(
            word in q
            for word in [
                "hostel",
                "bus",
                "transport",
                "mess",
                "outing"
            ]
        ):
            return "hostel"

        if any(
            word in q
            for word in [
                "placement",
                "job",
                "company",
                "internship",
                "event"
            ]
        ):
            return "placements"

        if any(
            word in q
            for word in [
                "admission",
                "apply",
                "eligibility",
                "eligible",
                "quota",
                "address",
                "contact",
                "phone",
                "email"
            ]
        ):
            return "admissions"

        return None

    def _search(self, question):
        if self.vectorizer is None or self.matrix is None:
            return None, None, 0.0

        try:
            normalized_question = self._norm(question)

            query_vector = self.vectorizer.transform(
                [normalized_question]
            )

            similarities = cosine_similarity(
                query_vector,
                self.matrix
            )[0]

            best_index = int(np.argmax(similarities))

            score = float(similarities[best_index])

            if score <= 0:
                return None, None, 0.0

            return (
                self.documents[best_index],
                self.sources[best_index],
                score
            )

        except Exception:
            return None, None, 0.0

    def _clean_answer(self, answer):
        if not answer:
            return answer

        answer = re.sub(
            r"\bBiomedical Engineering\b",
            "",
            answer,
            flags=re.IGNORECASE
        )

        return answer.strip()

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

    def ask(self, question):

        if not question or not question.strip():
            return {
                "answer": "Please enter a question.",
                "confidence": 0.0,
                "hits": []
            }

        question = question.strip()

        if self._is_fee_question(question):

            answer = self._get_fee_answer()

            self._log(
                question,
                1.0,
                "fees.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "fees.txt",
                        1.0
                    )
                ]
            }

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

        if self._is_admission_eligibility_question(question):

            answer = self._get_admission_eligibility_answer()

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

        if self._is_hostel_question(question):

            answer = self._get_hostel_answer()

            self._log(
                question,
                1.0,
                "hostel_transport.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "hostel_transport.txt",
                        1.0
                    )
                ]
            }

        if self._is_internship_question(question):

            answer = self._get_internship_answer()

            self._log(
                question,
                1.0,
                "placements_events.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "placements_events.txt",
                        1.0
                    )
                ]
            }

        if self._is_placement_question(question):

            answer = self._get_placement_answer()

            self._log(
                question,
                1.0,
                "placements_events.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "placements_events.txt",
                        1.0
                    )
                ]
            }

        if self._is_attendance_question(question):

            answer = self._get_attendance_answer()

            self._log(
                question,
                1.0,
                "exams_attendance.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "exams_attendance.txt",
                        1.0
                    )
                ]
            }

        if self._is_exam_question(question):

            answer = self._get_exam_answer()

            self._log(
                question,
                1.0,
                "exams_attendance.txt"
            )

            return {
                "answer": answer,
                "confidence": 1.0,
                "hits": [
                    (
                        answer,
                        "exams_attendance.txt",
                        1.0
                    )
                ]
            }

        category = self._detect_category(question)

        if category:

            category_file = self.files.get(category)

            if (
                category_file
                and os.path.exists(category_file)
            ):

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
                            local_vectorizer.fit_transform(
                                chunks
                            )
                        )

                        query_vector = (
                            local_vectorizer.transform(
                                [
                                    self._norm(question)
                                ]
                            )
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

        fallback = (
            "Sorry, I could not find a clear answer "
            "for that question. Please try asking "
            "about admissions, courses, fees, hostel, "
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

    def get_answer(self, question):
        return self.ask(question)
