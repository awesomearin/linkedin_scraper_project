import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit,
    QFileDialog, QMessageBox, QHBoxLayout
)

from linkedin_scraper import scrape_linkedin_job
from resume_scraper import extract_text_from_pdf, manual_experience_entry
from resume_matcher import match_resume_to_job
from suggester import generate_skill_suggestions

class ResumeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LinkedIn Scraper + Resume Parser")
        self.setMinimumWidth(600)

        self.layout = QVBoxLayout()

        # LinkedIn URL input
        self.url_label = QLabel("Enter LinkedIn Job URL:")
        self.url_input = QLineEdit()
        self.scrape_button = QPushButton("Scrape Job Info")
        self.scrape_button.clicked.connect(self.scrape_job)

        self.job_output = QTextEdit()
        self.job_output.setReadOnly(True)

        # Resume PDF upload
        self.resume_button = QPushButton("Upload Resume PDF")
        self.resume_button.clicked.connect(self.upload_resume)

        self.resume_output = QTextEdit()
        self.resume_output.setReadOnly(True)

        # Manual input
        self.manual_button = QPushButton("Enter Experience Manually")
        self.manual_button.clicked.connect(self.manual_entry)

        # Add widgets to layout
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.scrape_button)
        self.layout.addWidget(QLabel("🔎 Scraped Job Info:"))
        self.layout.addWidget(self.job_output)

        self.layout.addWidget(self.resume_button)
        self.layout.addWidget(QLabel("📄 Resume Text / Experience Preview:"))
        self.layout.addWidget(self.resume_output)

        self.layout.addWidget(self.manual_button)

        self.match_button = QPushButton("Match Resume to Job")
        self.match_button.clicked.connect(self.match_resume_to_job)
        self.layout.addWidget(self.match_button)

        self.match_output = QTextEdit()
        self.match_output.setReadOnly(True)
        self.layout.addWidget(QLabel("🎯 Resume Matching Result:"))
        self.layout.addWidget(self.match_output)
        self.suggest_button = QPushButton("💡 Generate GPT Suggestions")

        self.suggest_button.clicked.connect(self.generate_suggestions)
        self.layout.addWidget(self.suggest_button)

        self.suggestion_output = QTextEdit()
        self.suggestion_output.setReadOnly(True)
        self.layout.addWidget(QLabel("💬 AI Suggestions for Skill Gaps:"))
        self.layout.addWidget(self.suggestion_output)



        self.setLayout(self.layout)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def scrape_job(self):
        url = self.url_input.text().strip()
        result = scrape_linkedin_job(url)

        if "error" in result:
            self.show_error(result["error"])
        else:
            job_info = (
                f"Title: {result['title']}\n"
                f"Company: {result['company']}\n"
                f"Location: {result['location']}\n\n"
                f"Description:\n{result['description']}..."
            )
            self.job_output.setText(job_info)

    def upload_resume(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Resume PDF", "", "PDF Files (*.pdf)")
        if file_path:
            result = extract_text_from_pdf(file_path)
            if "error" in result:
                self.show_error(result["error"])
            else:
                self.resume_output.setText(result["text"])  # Preview
            
    def match_resume_to_job(self):
        job_text = self.job_output.toPlainText()
        resume_text = self.resume_output.toPlainText()

        if not job_text or not resume_text:
            self.show_error("Please scrape a job and load a resume or experience first.")
            return

        # Remove label headers from preview text if present
        clean_job = job_text.split("Description:")[-1]
        result = match_resume_to_job(clean_job, resume_text)

        output = f"✅ Match Score: {result['match_score']}%\n"
        output += "\n✅ Matched Skills:\n" + ", ".join(result['matched_skills']) if result['matched_skills'] else "\n(No matches)"
        output += "\n\n⚠️ Missing Skills:\n" + ", ".join(result['missing_skills']) if result['missing_skills'] else "\nNone!"

        self.match_output.setText(output)


    def manual_entry(self):
        entry = manual_experience_entry()
        self.resume_output.setText(str(entry))

    def generate_suggestions(self):
        job_text = self.job_output.toPlainText()
        resume_text = self.resume_output.toPlainText()

        if not job_text or not resume_text:
            self.show_error("You must match your resume to a job first.")
            return

        clean_job = job_text.split("Description:")[-1]
        result = match_resume_to_job(clean_job, resume_text)

        if not result["missing_skills"]:
            self.suggestion_output.setText("✅ No missing skills detected!")
            return

        suggestions = generate_skill_suggestions(clean_job, result["missing_skills"])
        self.suggestion_output.setText(suggestions)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResumeApp()
    window.show()
    sys.exit(app.exec_())
