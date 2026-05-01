from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(data, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Career Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Skills: {data['skills']}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"ATS Score: {data['score']}%", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Missing Skills: {data['missing']}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("AI Suggestions:", styles["Heading2"]))
    content.append(Paragraph(data['feedback'], styles["Normal"]))

    doc.build(content)

    return filename