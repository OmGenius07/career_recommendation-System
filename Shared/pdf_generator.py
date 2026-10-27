import json
import os
import time
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

def generate_pdf(recommendations):
    """
    Generate a PDF file in memory and return its bytes and a generated filename.
    """
    try:
        # Parse recommendations from JSON string if necessary
        if isinstance(recommendations, str):
            try:
                data = json.loads(recommendations)
            except json.JSONDecodeError:
                # Fallback for plain text or malformed JSON
                data = {"Career Recommendations": recommendations}
        else:
            data = recommendations

        # Generate a unique filename
        timestamp = str(int(time.time()))
        filename = f"career_plan_{timestamp}.pdf"

        # Create PDF in an in-memory buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        
        # Define styles
        styles = getSampleStyleSheet()
        heading = styles["Heading2"]
        subheading = ParagraphStyle(
            name="Subheading",
            parent=styles["Heading3"],
            textColor=colors.HexColor("#333333"),
            spaceBefore=6,
            spaceAfter=4,
        )
        body = styles["BodyText"]
        elements = []

        # Add Title
        elements.append(Paragraph("AI Career Path Recommendations", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Add Timestamp if available
        if isinstance(data, dict) and data.get("timestamp"):
            elements.append(Paragraph(f"Generated on: {data['timestamp']}", styles["Normal"]))
            elements.append(Spacer(1, 12))

        # Extract and add career paths
        career_paths = []
        if isinstance(data, dict):
            career_paths = data.get("career_paths") or data.get("paths") or []

        if isinstance(career_paths, list) and career_paths:
            elements.append(Paragraph("CAREER PATHS:", heading))
            elements.append(Spacer(1, 8))
            for idx, path in enumerate(career_paths):
                title = path.get("careerTitle", f"Career Option {idx + 1}")
                elements.append(Paragraph(f"{idx + 1}. {title}", heading))
                elements.append(Spacer(1, 6))

                # Skills
                skills = path.get("skillsToDevelop") or []
                if skills:
                    elements.append(Paragraph("Skills to develop:", subheading))
                    elements.append(ListFlowable([ListItem(Paragraph(str(skill), body)) for skill in skills], bulletType="bullet", leftIndent=18))
                    elements.append(Spacer(1, 4))

                # Certifications
                certs = path.get("recommendedCertifications") or []
                if certs:
                    elements.append(Paragraph("Recommended certifications:", subheading))
                    elements.append(ListFlowable([ListItem(Paragraph(str(cert), body)) for cert in certs], bulletType="bullet", leftIndent=18))
                    elements.append(Spacer(1, 4))

                # Short-term goals
                short_goals = path.get("shortTermGoals") or []
                if short_goals:
                    elements.append(Paragraph("Short-term goals (3-6 months):", subheading))
                    elements.append(ListFlowable([ListItem(Paragraph(str(goal), body)) for goal in short_goals], bulletType="bullet", leftIndent=18))
                    elements.append(Spacer(1, 4))

                # Long-term goals
                long_goals = path.get("longTermGoals") or []
                if long_goals:
                    elements.append(Paragraph("Long-term goals (1-3 years):", subheading))
                    elements.append(ListFlowable([ListItem(Paragraph(str(goal), body)) for goal in long_goals], bulletType="bullet", leftIndent=18))
                    elements.append(Spacer(1, 4))

                elements.append(Spacer(1, 8))
        else:
            # Fallback for unstructured data
            for key, value in (data.items() if isinstance(data, dict) else [("Recommendations", data)]):
                elements.append(Paragraph(f"{key}", heading))
                if isinstance(value, list):
                    elements.append(ListFlowable([ListItem(Paragraph(str(item), body)) for item in value], bulletType="bullet", leftIndent=18))
                else:
                    elements.append(Paragraph(str(value), body))
                elements.append(Spacer(1, 8))

        # Add Footer
        elements.append(Spacer(1, 16))
        elements.append(Paragraph("End of Career Recommendations", styles["Normal"]))

        # Build the PDF document
        doc.build(elements)
        
        # Get the PDF content from the buffer
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # Return the PDF bytes and the filename
        return pdf_bytes, filename

    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Return None to indicate failure
        return None, None
