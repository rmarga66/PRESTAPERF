import streamlit as st
from PIL import Image
from fpdf import FPDF
from io import BytesIO

# Hardcoded data from the simplified Excel file
sheet_data = [
    {"Indication": "SA", "Designation": "Perf a dom, forf Perfusion à domicile, forf instal1, syst actif électrique, PERFADOM1-I1-SA-ELEC", "Tarif_HT": 297.67},
    {"Indication": "SA", "Designation": "Perf a dom, forf instal2, système actif élec, PERFADOM2-I2-SA-ELEC", "Tarif_HT": 137.38},
    # (Add remaining rows here...)
]

indications = list(set(item["Indication"] for item in sheet_data))

# Load logo
logo = Image.open("logo.png")  # Ensure logo.png is in the same folder as this script

# Streamlit UI
st.image(logo, width=150)
st.title("PRESTAPERF Calculator")
st.sidebar.header("Configuration")

# Session state initialization
if "details" not in st.session_state:
    st.session_state.details = []
if "total" not in st.session_state:
    st.session_state.total = 0
if "client_sap" not in st.session_state:
    st.session_state.client_sap = ""

# Indications Selection
selected_indications = st.sidebar.multiselect("Choisissez les indications", options=indications)

# Filtered Designations
designations = [item for item in sheet_data if item["Indication"] in selected_indications]
designation_quantities = {}

if selected_indications:
    st.subheader("Désignations")
    for item in designations:
        designation = item["Designation"]
        quantity = st.number_input(f"Quantité pour {designation}", min_value=0, step=1, key=designation)
        designation_quantities[designation] = (quantity, item["Tarif_HT"])

if st.button("Calculer"):
    st.session_state.details = []
    st.session_state.total = 0

    for designation, (quantity, tarif_ht) in designation_quantities.items():
        if quantity > 0:
            cost = tarif_ht * quantity
            st.session_state.total += cost
            st.session_state.details.append(f"{designation}: {quantity} x {tarif_ht}€ HT = {cost:.2f}€ HT")

    st.success("Calcul terminé !")

# Display calculation details
if st.session_state.details:
    st.subheader("Détail des désignations")
    for detail in st.session_state.details:
        st.write(detail)

    st.subheader("Total")
    st.write(f"Total HT: {st.session_state.total:.2f}€")

# Generate Invoice
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

# Invoice generation button
st.session_state.client_sap = st.text_input("Numéro Client SAP", st.session_state.client_sap)
if st.session_state.details and st.session_state.client_sap:
    if st.button("Générer Fact
