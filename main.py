import streamlit as st
from fpdf import FPDF

# Hardcoded data from the simplified Excel file
sheet_data = [
    {"Indication": "SA", "Designation": "Perf a dom, forf Perfusion à domicile, forf instal1, syst actif électrique, PERFADOM1-I1-SA-ELEC", "Tarif_HT": 297.67},
    {"Indication": "SA", "Designation": "Perf a dom, forf instal2, système actif élec, PERFADOM2-I2-SA-ELEC", "Tarif_HT": 137.38},
    {"Indication": "SA", "Designation": "Perf a dom, forf ins rempli par ES, syst actif élec, PERFADOM3-I-REMPLI-ES-SA-ELEC", "Tarif_HT": 137.38},
    {"Indication": "DIFF", "Designation": "Perf a dom, forf instal1, diffuseur, PERFADOM4-I1-DIFF", "Tarif_HT": 190.81},
    {"Indication": "DIFF", "Designation": "Perf a dom, forf instal2, diffuseur, PERFADOM5-I2-DIFF", "Tarif_HT": 87.77},
    {"Indication": "GRAV", "Designation": "Perf a dom, forfait instal et suivi, gravité, PERFADOM6-IS-GRAV", "Tarif_HT": 38.16},
    {"Indication": "SA", "Designation": "Perf a dom, forfait hebdo suivi, système actif, PERFADOM7E-S-SA-ELEC", "Tarif_HT": 83.95},
    {"Indication": "DIFF", "Designation": "Perf a dom, forfait hebdo suivi, diffuseur, PERFADOM8-S-DIFF", "Tarif_HT": 38.16},
    {"Indication": "GRAV", "Designation": "Perf a dom, forf/ perf consom-access, Gravité, < 15 perf, PERFADOM17-C-GRAV < 15/ 28J", "Tarif_HT": 9},
    {"Indication": "GRAV", "Designation": "Perf a dom, forf hebdo consom-access, Gravité, 1 perf/ j, PERFADOM18-C-GRAV = 1/ J", "Tarif_HT": 63.35},
    {"Indication": "GRAV", "Designation": "Perf à dom, forf hebdo consom-access, Gravité, 2 perf/ j, PERFADOM19-C-GRAV = 2/ J", "Tarif_HT": 119.83},
    {"Indication": "GRAV", "Designation": "Perf à dom, forf hebdo consom-access, Gravité, > 2 perf/ j, PERFADOM20-C-GRAV > 2/ J", "Tarif_HT": 170.2},
    {"Indication": "VVC", "Designation": "Perf à dom, forf d'entret voie centrale, PERFADOM21-ENTRETIEN-VC-SF-PICC", "Tarif_HT": 7.63},
    {"Indication": "PICC", "Designation": "Perf à dom, forfait d'ent voie centrale, PERFADOM22-ENTRETIEN-VC-PICC-LINE", "Tarif_HT": 14.88},
    {"Indication": "DIFF", "Designation": "Perf à dom, forf hebdo consom-access, débr diff étab sant, PERFADOM24-C-DEBR-DIFF", "Tarif_HT": 11.5},
    {"Indication": "SA", "Designation": "Perf a dom, forf hebdo consom-access, systeme actif,1perf/s, PERFA-DOM27-C-SA=1/S", "Tarif_HT": 28.97},
    {"Indication": "SA", "Designation": "Perf a dom, forf heb consom-access, systeme actif,2a3perf/s, PERFA-DOM28-C-SA=2A3/S", "Tarif_HT": 57.92},
    {"Indication": "SA", "Designation": "Perf a dom, forf heb consom-access, systeme actif,4a6perf/s, PERFA-DOM29-C-SA=4A6/S", "Tarif_HT": 130.33},
    {"Indication": "SA", "Designation": "Perf a dom, forf hebdo consom-access, systeme actif,1 perf/j, PERFA-DOM30-C-SA=1/J", "Tarif_HT": 200.12},
    {"Indication": "SA", "Designation": "Perf a dom, forf hebdo consom-access, systeme actif,2 perf/j, PERFA-DOM31-C-SA=2/J", "Tarif_HT": 379.14},
    {"Indication": "SA", "Designation": "Perf a dom, forf hebdo consom-access, systeme actif,3 perf/j, PERFA-DOM32-C-SA=3/J", "Tarif_HT": 539.39},
    {"Indication": "SA", "Designation": "Perf a  dom, forf hebdo consom-access, systeme actif, >3 perf/j, PERFADOM33-C-SA>3/J", "Tarif_HT": 679.32},
    {"Indication": "DIFF", "Designation": "Perf a  dom, forf hebdo consom-access, diffuseur,1 perf/s, PERFA-DOM34-C-DIFF=1/S", "Tarif_HT": 26.06},
    {"Indication": "DIFF", "Designation": "Perf a dom, forf heb consom-access, diffuseur,2a3perf/s, PERFADOM35-C-DIFF=2A3/S", "Tarif_HT": 52.12},
    {"Indication": "DIFF", "Designation": "Perf a dom, forf heb consom-access, diffuseur,4a6perf/s, PERFADOM36-C-DIFF=4A6/S", "Tarif_HT": 117.29},
    {"Indication": "DIFF", "Designation": "Perf a  dom, forf hebdo consom-access, diffuseur,1 perf/j, PERFA-DOM37-C-DIFF=1/J", "Tarif_HT": 180.1},
    {"Indication": "DIFF", "Designation": "Perf a  dom, forf hebdo consom-access, diffuseur,2 perf/j, PERFA-DOM38-C-DIFF=2/J", "Tarif_HT": 341.22},
    {"Indication": "DIFF", "Designation": "Perf a  dom, forf hebdo consom-access, diffuseur,3 perf/j, PERFA-DOM39-C-DIFF=3/J", "Tarif_HT": 485.45},
    {"Indication": "DIFF", "Designation": "Perf a dom, forf hebdo consom-access, diffuseur, >3 perf/j, PERFA-DOM40-C-DIFF>3/J", "Tarif_HT": 611.38},
    {"Indication": "IMMUNO SC", "Designation": "Perf a dom, forf heb consom-access, systeme actif,1perf/s, PERFA-DOM41-C-SA IMMU-SC", "Tarif_HT": 39.96},
    {"Indication": "IMMUNO IV", "Designation": "Perf a dom, forf consom-access, systeme actif,1perf/j, PERFADOM42-C-SA IMMU-IV", "Tarif_HT": 39.96},
    {"Indication": "SA", "Designation": "Perf à dom, forf hebdo consom-access, débr SA étab sant, PERFADOM45-C-DEBR-SA", "Tarif_HT": 11.5},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale, forfait de première installation", "Tarif_HT": 325},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale, forfait d’installation après perfusion à domicile", "Tarif_HT": 144.62},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale, sans entérale associée, pompe, prest° hebd., pdt 12 prem. Sem", "Tarif_HT": 75},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale, sans entérale associée, pompe, prest° hebd., après 12 prem. Sem", "Tarif_HT": 58.33},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale 6 ou 7 j/7, consommables et accessoires, forfait.", "Tarif_HT": 158.33},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale < = 5 j/7 avec entérale, pompe(s), prest° hebd, pdt 12 prem sem", "Tarif_HT": 116.67},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale < = 5 j/7 avec entérale, pompe(s), prest° hebd, après 12 prem sem", "Tarif_HT": 100},
    {"Indication": "NUT PAR", "Designation": "Nutrition parentérale < = 5 j/7, consommables et accessoires, npad, forfait", "Tarif_HT": 95.84},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, forfait de première installation.", "Tarif_HT": 146.53},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, forfait hebdomadaire sans pompe ou par gravité", "Tarif_HT": 50.33},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, forfait hebdomadaire avec pompe", "Tarif_HT": 68.52}
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
