import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit,
    QFileDialog, QMessageBox, QHBoxLayout
)

from linkedin_scraper import scrape_linkedin_job
from resume_scraper import extract_text_from_pdf, manual_experience_entry

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
                f"Description:\n{result['description'][:1000]}..."
            )
            self.job_output.setText(job_info)

    def upload_resume(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Resume PDF", "", "PDF Files (*.pdf)")
        if file_path:
            result = extract_text_from_pdf(file_path)
            if "error" in result:
                self.show_error(result["error"])
            else:
                self.resume_output.setText(result["text"][:3000])  # Preview

    def manual_entry(self):
        entry = manual_experience_entry()
        self.resume_output.setText(str(entry))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResumeApp()
    window.show()
    sys.exit(app.exec_())
