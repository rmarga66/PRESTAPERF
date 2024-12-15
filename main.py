from fpdf import FPDF
from io import BytesIO
import streamlit as st

def generate_invoice(details, total, client_sap):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.set_fill_color(224, 224, 224)  # Light gray
    pdf.cell(200, 10, "FACTURE", ln=True, align="C", fill=True)
    pdf.ln(10)

    # Client Information
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, f"Client SAP: {client_sap}", ln=True, align="L")
    pdf.ln(10)

    # Details
    pdf.cell(200, 10, "Détails des désignations:", ln=True, align="L")
    pdf.set_font("Arial", size=9)

    for line in details:
        pdf.multi_cell(0, 10, line)

    pdf.ln(10)

    # Total
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total HT: {total:.2f}€", ln=True, align="L")

    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", size=8)
    pdf.cell(200, 10, "Merci pour votre confiance.", ln=True, align="C")

    # Save to buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# Generate PDF button
if st.session_state.details and st.session_state.client_sap:
    if st.button("Générer Facture"):
        pdf_buffer = generate_invoice(st.session_state.details, st.session_state.total, st.session_state.client_sap)
        st.download_button(
            "Télécharger la Facture",
            data=pdf_buffer,
            file_name="facture.pdf",
            mime="application/pdf"
        )
else:
    st.write("Veuillez remplir les informations nécessaires pour générer une facture.")
