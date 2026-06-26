import random
import xml.etree.ElementTree as ET
from faker import Faker

fake = Faker("el_GR")          # ελληνικά ονόματα
Faker.seed(42)                 # ίδια "τυχαία" δεδομένα κάθε φορά (αναπαραγωγιμότητα)
random.seed(42)

N = 1000                       # πόσες εγγραφές θέλουμε
VALID_INCOME_TYPES = ["INTEREST", "DIVIDEND", "REPO", "BOND_INTEREST", "DEPOSIT"]

root = ET.Element("Submissions")

for i in range(N):
    rec = ET.SubElement(root, "Record")

    # --- ΑΦΜ: συνήθως σωστό (9 ψηφία), μερικές φορές "χαλασμένο" ---
    r = random.random()
    if r < 0.05:
        afm = ""                                   # κενό (λάθος)
    elif r < 0.10:
        afm = str(random.randint(10000000, 99999999))  # 8 ψηφία (λάθος)
    else:
        afm = str(random.randint(100000000, 999999999)) # 9 ψηφία (σωστό)

    # --- Όνομα/επώνυμο: μερικές φορές λείπουν ---
    last_name = "" if random.random() < 0.03 else fake.last_name()
    first_name = "" if random.random() < 0.03 else fake.first_name()

    # --- Τύπος εισοδήματος: μερικές φορές εκτός λίστας ---
    if random.random() < 0.04:
        income_type = "UNKNOWN"                    # μη επιτρεπτό (λάθος)
    else:
        income_type = random.choice(VALID_INCOME_TYPES)

    # --- Ποσό: μερικές φορές αρνητικό ή μηδέν ---
    if random.random() < 0.05:
        amount = round(random.uniform(-500, 0), 2) # <= 0 (λάθος)
    else:
        amount = round(random.uniform(10, 50000), 2)

    # --- Έτος αναφοράς: μερικές φορές παράλογο ---
    if random.random() < 0.03:
        reference_year = random.choice([1850, 2099])  # λάθος
    else:
        reference_year = random.choice([2022, 2023, 2024])

    ET.SubElement(rec, "Afm").text = afm
    ET.SubElement(rec, "LastName").text = last_name
    ET.SubElement(rec, "FirstName").text = first_name
    ET.SubElement(rec, "IncomeType").text = income_type
    ET.SubElement(rec, "Amount").text = str(amount)
    ET.SubElement(rec, "ReferenceYear").text = str(reference_year)

# Γράψιμο σε αρχείο XML
tree = ET.ElementTree(root)
ET.indent(tree, space="  ")     # όμορφη στοίχιση
tree.write("data/pol1033_submission.xml", encoding="utf-8", xml_declaration=True)

print(f"Δημιουργήθηκαν {N} εγγραφές στο data/pol1033_submission.xml")