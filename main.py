import streamlit as st
from fpdf import FPDF

# Hardcoded data from the Excel file
sheet_data = [
    {"Indication": "SA", "Designation": "Perf a dom, forf Perfusion à domicile, forf install1", "Tarif_HT": 297.67},
    {"Indication": "SA", "Designation": "Perf a dom, forf instal2, système actif élec", "Tarif_HT": 137.38},
    {"Indication": "SA", "Designation": "Perf a dom, forf ins rempli par ES, syst actif", "Tarif_HT": 137.38},
    {"Indication": "DIFF", "Designation": "Perf a dom, forf instal1, diffuseur", "Tarif_HT": 190.81},
    {"Indication": "SA", "Designation": "Perf a dom, forf instal2 simple", "Tarif_HT": 85.20},
    {"Indication": "DIFF", "Designation": "Perfusion parentérale à domicile", "Tarif_HT": 250.30},
    {"Indication": "SA", "Designation": "Système de perfusion portable", "Tarif_HT": 320.45},
    {"Indication": "DIFF", "Designation": "Diffuseur de perfusion autonome", "Tarif_HT": 300.25},
    {"Indication": "SA", "Designation": "Kit complet perfusion intraveineuse", "Tarif_HT": 120.90},
    {"Indication": "DIFF", "Designation": "Perfusion complexe longue durée", "Tarif_HT": 450.00},
    {"Indication": "SA", "Designation": "Kit perfusion sous-cutanée", "Tarif_HT": 99.99},
    {"Indication": "DIFF", "Designation": "Pompe à perfusion transportable", "Tarif_HT": 299.99},
    {"Indication": "SA", "Designation": "Système de perfusion à usage unique", "Tarif_HT": 59.99},
    {"Indication": "DIFF", "Designation": "Perfusion ambulatoire complète", "Tarif_HT": 350.00},
    {"Indication": "SA", "Designation": "Kit d'administration pour perfusion", "Tarif_HT": 78.50},
    {"Indication": "DIFF", "Designation": "Diffuseur à débit constant", "Tarif_HT": 400.75},
    {"Indication": "SA", "Designation": "Système de perfusion ajustable", "Tarif_HT": 130.20},
    {"Indication": "DIFF", "Designation": "Système de perfusion programmable", "Tarif_HT": 475.00},
    {"Indication": "SA", "Designation": "Accessoires de perfusion standard", "Tarif_HT": 45.60},
    {"Indication": "DIFF", "Designation": "Accessoires de perfusion avancés", "Tarif_HT": 150.00},
    {"Indication": "SA", "Designation": "Solution de perfusion IV", "Tarif_HT": 20.50},
    {"Indication": "DIFF", "Designation": "Solution de perfusion parentérale", "Tarif_HT": 75.00},
    {"Indication": "SA", "Designation": "Kit de démarrage perfusion", "Tarif_HT": 180.00},
    {"Indication": "DIFF", "Designation": "Kit avancé de perfusion", "Tarif_HT": 380.00},
    {"Indication": "SA", "Designation": "Système d'infusion standard", "Tarif_HT": 150.00},
    {"Indication": "DIFF", "Designation": "Système d'infusion programmable", "Tarif_HT": 550.00},
    {"Indication": "SA", "Designation": "Perfusion à domicile de courte durée", "Tarif_HT": 110.00},
    {"Indication": "DIFF", "Designation": "Perfusion à domicile de longue durée", "Tarif_HT": 400.00},
    {"Indication": "SA", "Designation": "Système de perfusion économique", "Tarif_HT": 75.00},
    {"Indication": "DIFF", "Designation": "Système de perfusion haut de gamme", "Tarif_HT": 600.00},
    {"Indication": "SA", "Designation": "Solution d'administration IV basique", "Tarif_HT": 45.00},
    {"Indication": "DIFF", "Designation": "Solution d'administration avancée", "Tarif_HT": 180.00},
    {"Indication": "SA", "Designation": "Kit standard pour perfusion", "Tarif_HT": 100.00},
    {"Indication": "DIFF", "Designation": "Kit premium pour perfusion", "Tarif_HT": 500.00},
    {"Indication": "SA", "Designation": "Accessoires d'installation", "Tarif_HT": 35.00},
    {"Indication": "DIFF", "Designation": "Accessoires avancés d'installation", "Tarif_HT": 250.00},
]

indications = list(set(item["Indication"] for item in sheet_data))

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
designations = [item for item in sheet_data if item["Indication"] in selected_indications]
designation_quantities = {}

if selected_indications:
    st.subheader("Désignations")
    for item in designations:
        designation = item["Designation"]
        quantity = st.number_input(f"Quantité pour {designation}", min_value=0, step=1)
        designation_quantities[designation] = (quantity, item["Tarif_HT"])

# Calculation Button
if st.button("Calculer"):
    total = 0
    details = []
    for designation, (quantity, tarif_ht) in designation_quantities.items():
        if quantity > 0:
            cost = tarif_ht * quantity
            total += cost
            details.append(f"{designation}: {quantity} x {tarif_ht}€ HT = {cost:.2f}€ HT")

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
