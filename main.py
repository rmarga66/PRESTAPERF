import streamlit as st
from PIL import Image

# Hardcoded data from the simplified Excel file
sheet_data = [
    {"Indication": "SA", "Designation": "forf Perfusion à domicile, forf instal1, syst actif électrique, PERFADOM1-I1-SA-ELEC", "Tarif_HT": 297.67},
    {"Indication": "SA", "Designation": "forf instal2, système actif élec, PERFADOM2-I2-SA-ELEC", "Tarif_HT": 137.38},
    {"Indication": "SA", "Designation": "forf ins rempli par ES, syst actif élec, PERFADOM3-I-REMPLI-ES-SA-ELEC", "Tarif_HT": 137.38},
    {"Indication": "DIFF", "Designation": "forf instal1, diffuseur, PERFADOM4-I1-DIFF", "Tarif_HT": 190.81},
    {"Indication": "DIFF", "Designation": "forf instal2, diffuseur, PERFADOM5-I2-DIFF", "Tarif_HT": 87.77},
    {"Indication": "GRAV", "Designation": "forfait instal et suivi, gravité, PERFADOM6-IS-GRAV", "Tarif_HT": 38.16},
    {"Indication": "SA", "Designation": "forfait hebdo suivi, système actif, PERFADOM7E-S-SA-ELEC", "Tarif_HT": 83.95},
    {"Indication": "DIFF", "Designation": "forfait hebdo suivi, diffuseur, PERFADOM8-S-DIFF", "Tarif_HT": 38.16},
    {"Indication": "GRAV", "Designation": "forf/ perf consom-access, Gravité, < 15 perf, PERFADOM17-C-GRAV < 15/ 28J", "Tarif_HT": 9},
    {"Indication": "GRAV", "Designation": "forf hebdo consom-access, Gravité, 1 perf/ j, PERFADOM18-C-GRAV = 1/ J", "Tarif_HT": 63.35},
    {"Indication": "GRAV", "Designation": "forf hebdo consom-access, Gravité, 2 perf/ j, PERFADOM19-C-GRAV = 2/ J", "Tarif_HT": 119.83},
    {"Indication": "GRAV", "Designation": "forf hebdo consom-access, Gravité, > 2 perf/ j, PERFADOM20-C-GRAV > 2/ J", "Tarif_HT": 170.2},
    {"Indication": "VVC", "Designation": "forf d'entret voie centrale, PERFADOM21-ENTRETIEN-VC-SF-PICC", "Tarif_HT": 7.63},
    {"Indication": "PICC", "Designation": "forfait d'ent voie centrale, PERFADOM22-ENTRETIEN-VC-PICC-LINE", "Tarif_HT": 14.88},
    {"Indication": "DIFF", "Designation": "forf hebdo consom-access, débr diff étab sant, PERFADOM24-C-DEBR-DIFF", "Tarif_HT": 11.5},
    {"Indication": "SA", "Designation": "forf hebdo consom-access, systeme actif,1perf/s, PERFA-DOM27-C-SA=1/S", "Tarif_HT": 28.97},
    {"Indication": "SA", "Designation": "forf heb consom-access, systeme actif,2a3perf/s, PERFA-DOM28-C-SA=2A3/S", "Tarif_HT": 57.92},
    {"Indication": "SA", "Designation": "forf heb consom-access, systeme actif,4a6perf/s, PERFA-DOM29-C-SA=4A6/S", "Tarif_HT": 130.33},
    {"Indication": "SA", "Designation": "forf hebdo consom-access, systeme actif,1 perf/j, PERFA-DOM30-C-SA=1/J", "Tarif_HT": 200.12},
    {"Indication": "SA", "Designation": "forf hebdo consom-access, systeme actif,2 perf/j, PERFA-DOM31-C-SA=2/J", "Tarif_HT": 379.14},
    {"Indication": "SA", "Designation": "forf hebdo consom-access, systeme actif,3 perf/j, PERFA-DOM32-C-SA=3/J", "Tarif_HT": 539.39},
    {"Indication": "SA", "Designation": "forf hebdo consom-access, systeme actif, >3 perf/j, PERFADOM33-C-SA>3/J", "Tarif_HT": 679.32},
    {"Indication": "DIFF", "Designation": "forf hebdo consom-access, diffuseur,1 perf/s, PERFA-DOM34-C-DIFF=1/S", "Tarif_HT": 26.06},
    {"Indication": "DIFF", "Designation": "forf heb consom-access, diffuseur,2a3perf/s, PERFADOM35-C-DIFF=2A3/S", "Tarif_HT": 52.12},
    {"Indication": "DIFF", "Designation": "forf heb consom-access, diffuseur,4a6perf/s, PERFADOM36-C-DIFF=4A6/S", "Tarif_HT": 117.29},
    {"Indication": "DIFF", "Designation": "forf hebdo consom-access, diffuseur,1 perf/j, PERFA-DOM37-C-DIFF=1/J", "Tarif_HT": 180.1},
    {"Indication": "DIFF", "Designation": "forf hebdo consom-access, diffuseur,2 perf/j, PERFA-DOM38-C-DIFF=2/J", "Tarif_HT": 341.22},
    {"Indication": "DIFF", "Designation": "forf hebdo consom-access, diffuseur,3 perf/j, PERFA-DOM39-C-DIFF=3/J", "Tarif_HT": 485.45},
    {"Indication": "DIFF", "Designation": "forf hebdo consom-access, diffuseur, >3 perf/j, PERFA-DOM40-C-DIFF>3/J", "Tarif_HT": 611.38},
    {"Indication": "IMMUNO SC", "Designation": "forf heb consom-access, systeme actif,1perf/s, PERFA-DOM41-C-SA IMMU-SC", "Tarif_HT": 39.96},
    {"Indication": "IMMUNO IV", "Designation": "forf consom-access, systeme actif,1perf/j, PERFADOM42-C-SA IMMU-IV", "Tarif_HT": 39.96},
    {"Indication": "SA", "Designation": "forf hebdo consom-access, débr SA étab sant, PERFADOM45-C-DEBR-SA", "Tarif_HT": 11.5},
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
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, forfait hebdomadaire avec pompe", "Tarif_HT": 68.52},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, vente 500ml normocal", "Tarif_HT": 3.11},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, vente 500ml hypercal", "Tarif_HT": 3.61},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, vente 500ml hyperprot, hypercal", "Tarif_HT": 3.65},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, vente 500ml 2kcal", "Tarif_HT": 4.20},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, Sonde de remplacement gastrostomie(4/an)", "Tarif_HT": 32.92},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, Sonde silicone (1/mois)", "Tarif_HT": 4.37},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, Sonde PVC (1/24h)", "Tarif_HT": 0.49},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, Set Gastro ASEPT", "Tarif_HT": 34.16},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, Bouton (4/an)", "Tarif_HT": 231.20},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, Prolongateur (bouton 1/sem)", "Tarif_HT": 10.83},
    {"Indication": "NUT ENT", "Designation": "Nutrition entérale, Set SNG pédia", "Tarif_HT": 59.72},
]

indications = list(set(item["Indication"] for item in sheet_data))

# Load logo
logo = Image.open("logo.png")  # Replace "logo.png" with the path to your logo file

# Streamlit UI
st.image(logo, width=150)
st.title("Calculette - PRESTAPERF")
st.sidebar.header("Bonjour,")

# Sidebar instructions
st.sidebar.markdown(
    "<p style='color:red; font-style:italic;'>"
    "AIDE MEMOIRE :<br>"
    "- Un seul forfait de première installation en nutrition entérale (dans une vie)<br>"
    "- Choisir le forfait le plus rémunérateur (pour celui d'installation et pour celui de suivi)<br>"
    "- Pas plus de 4 perfusions/j d'un même dispositif (SA/Diff)<br>"
    "- Possibilité de cumuler 4 perfusions d'un dispositif (SA et Diff) et 1 d'un autre(Gravité)<br>"
    "- Forfait Installation 2 : applicable 4j après le forfait de 1ère installation, pour un autre dispositif"
    "</p>",
    unsafe_allow_html=True,
)

# Session state initialization
if "details" not in st.session_state:
    st.session_state.details = []
if "total" not in st.session_state:
    st.session_state.total = 0

# Indications Selection
selected_indications = st.sidebar.multiselect("Choisissez les dispositifs du patient", options=indications)

# Filtered Designations
designations = [item for item in sheet_data if item["Indication"] in selected_indications]
designation_quantities = {}

if selected_indications:
    st.subheader("PERFADOM")
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

    st.success("Calcul terminé, c'est de la bombe bébé !")

# Display calculation details
if st.session_state.details:
    st.subheader("Détail de ta facture")
    for detail in st.session_state.details:
        st.write(detail)

    st.subheader("Total")
    st.write(f"Total HT: {st.session_state.total:.2f}€")
    st.write("Fait par Romain Margalet")
    st.write("Tu n'es pas sûr de ton calcul, je peux t'aider : romain.margalet@bastide-medical.fr")
    
