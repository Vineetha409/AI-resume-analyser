from flask import Flask, request, render_template
import pdfplumber

app = Flask(__name__)

skills = ["python","java","c","html","css","javascript","sql","machine learning","data science","git"]

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text.lower()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['resume']
    text = extract_text(file)

    found = []
    missing = []

    for skill in skills:
        if skill in text:
            found.append(skill)
        else:
            missing.append(skill)

    score = round(len(found) / len(skills) * 100)

    suggestions = []
    for skill in missing:
        suggestions.append("Add " + skill + " skill to improve your resume.")

    # Predict job role
    job_role = "General Software Developer"

    if "machine learning" in text or "data science" in text:
        job_role = "Data Scientist"

    elif "html" in text or "css" in text or "javascript" in text:
        job_role = "Web Developer"

    elif "python" in text and "sql" in text:
        job_role = "Backend Developer"

    return render_template(
        "result.html",
        score=score,
        found=found,
        missing=missing,
        suggestions=suggestions,
        job_role=job_role
    )


if __name__ == "__main__":
    app.run(debug=True)