import requests
from fpdf import FPDF

# Gist raw URL
GIST_URL = "https://gist.githubusercontent.com/wisamalabed/6c826f000b9d865a34c0ba6a4841cdb1/raw"

# Fetch JSON
data = requests.get(GIST_URL).json()

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Add TrueType Unicode font
pdf.add_font("OpenSans", "", "fonts/OpenSans-Regular.ttf")
pdf.add_font("OpenSans", "B", "fonts/OpenSans-Bold.ttf")
pdf.add_font("OpenSans", "I", "fonts/OpenSans-Italic.ttf")

# Example usage


pdf.set_font("OpenSans", "", 12)   # Regular for body text

# ----- Basics -----
basics = data.get("basics", {})
pdf.set_font("OpenSans", "B", 20)  # Bold for name
pdf.cell(0, 10, basics.get("name", ""), ln=1)

pdf.set_font("OpenSans", "I", 14)  # Italic for label
pdf.multi_cell(0, 8, basics.get("label", ""))
pdf.ln(2)

contact_info = f"{basics.get('email','')} | {basics.get('phone','')} | {basics.get('location', {}).get('city','')}, {basics.get('location', {}).get('countryCode','')}"
pdf.set_font("OpenSans", "", 12)   # Regular for body text
pdf.multi_cell(0, 6, contact_info)
pdf.ln(5)

summary = basics.get("summary", "")
pdf.multi_cell(0, 6, summary)
pdf.ln(5)

# ----- Education -----
pdf.set_font("OpenSans", "B", 16)
pdf.cell(0, 10, "Education", ln=1)
pdf.set_font("OpenSans", "", 12)   # Regular for body text
for edu in data.get("education", []):
    institution = edu.get("institution", "")
    degree = edu.get("studyType", "")
    area = edu.get("area", "")
    start = edu.get("startDate", "")
    end = edu.get("endDate", "")
    pdf.multi_cell(0, 6, f"{degree} in {area}, {institution} ({start} - {end})")
pdf.ln(5)

# ----- Skills -----
pdf.set_font("OpenSans", "B", 16)
pdf.cell(0, 10, "Skills", ln=1)
pdf.set_font("OpenSans", "", 12)   # Regular for body text
for skill in data.get("skills", []):
    name = skill.get("name", "")
    keywords = ", ".join(skill.get("keywords", []))
    pdf.multi_cell(0, 6, f"{name} ({skill.get('level','')}): {keywords}")
pdf.ln(5)

# ----- Work Experience -----
pdf.set_font("OpenSans", "B", 16)
pdf.cell(0, 10, "Work Experience", ln=1)
pdf.set_font("OpenSans", "", 12)   # Regular for body text
for work in data.get("work", []):
    position = work.get("position", "")
    company = work.get("name", "")
    location = work.get("location", "")
    start = work.get("startDate", "")
    end = work.get("endDate", "Present")
    pdf.set_font("OpenSans", "B", 12)
    pdf.multi_cell(0, 6, f"{position}, {company} ({start} - {end})")
    
    pdf.set_font("OpenSans", "", 12)   # Regular for body text
    summary = work.get("summary", "")
    pdf.multi_cell(0, 6, summary)
    
    highlights = work.get("highlights", [])
    if highlights:
        for h in highlights:
            pdf.multi_cell(0, 6, f"  - {h}")
    pdf.ln(3)

# Save PDF
pdf.output("resume.pdf")
print("✅ resume.pdf generated successfully!")