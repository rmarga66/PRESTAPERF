import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load data from the Excel file directly
file_path = '/mnt/data/PERFADOM Janvier 23.xlsx'
sheet_data = pd.ExcelFile(file_path).parse('Feuil1')

# Process data
sheet_data.columns = sheet_data.iloc[0]
sheet_data = sheet_data[1:]
sheet_data = sheet_data.rename(columns={
    'INDICATION': 'Indication',
    'DÉSIGNATION': 'Designation',
    'Tarif HT': 'Tarif_HT'
})

indications = sheet_data['Indication'].drop_duplicates().tolist()

# Streamlit UI
st.title("PRESTAPERF Calculator")
st.sidebar.header("Configuration")

def generate_pdf(details, total, client_sap):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_fill_color(224, 255, 255)  # Turquoise
    pdf.set_text_color(255, 69, 0)  # Rouge
    pdf.cell(200, 10, txt="PRESTAPERF - Résumé", ln=True, align="C", fill=True)

    pdf.set_text_color(0, 0, 0)  # Noir
    pdf.cell(200, 10, txt=f"Numéro Client SAP: {client_sap}", ln=True, align="L")

    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Détail des désignations:", ln=True, align="L")

    for line in details:
        pdf.cell(200, 10, txt=line, ln=True, align="L")

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total HT: {total:.2f}€", ln=True, align="L")

    pdf_file_path = "PRESTAPERF_Resume.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path

# Indications Selection
selected_indications = st.sidebar.multiselect("Choisissez les indications", options=indications)

# Filtered Designations
designations = sheet_data[sheet_data['Indication'].isin(selected_indications)]['Designation'].drop_duplicates().tolist()
designation_quantities = {}

if selected_indications:
    st.subheader("Désignations")
    for designation in designations:
        quantity = st.number_input(f"Quantité pour {designation}", min_value=0, step=1)
        designation_quantities[designation] = quantity

# Calculation Button
if st.button("Calculer"):
    total = 0
    details = []
    for designation, quantity in designation_quantities.items():
        if quantity > 0:
            row = sheet_data[sheet_data['Designation'] == designation].iloc[0]
            cost = float(row['Tarif_HT']) * quantity
            total += cost
            details.append(f"{designation}: {quantity} x {row['Tarif_HT']}€ HT = {cost:.2f}€ HT")

    st.subheader("Détail des désignations")
    for detail in details:
        st.write(detail)

    st.subheader("Total")
    st.write(f"Total HT: {total:.2f}€")

    # PDF Generation
    client_sap = st.text_input("Numéro Client SAP")
    if st.button("Générer PDF"):
        if client_sap:
            pdf_path = generate_pdf(details, total, client_sap)
            st.success(f"PDF généré avec succès: {pdf_path}")
            with open(pdf_path, "rb") as pdf_file:
                st.download_button("Télécharger le PDF", data=pdf_file, file_name="PRESTAPERF_Resume.pdf")
        else:
            st.error("Veuillez renseigner le numéro client SAP.")
