import re

def format_invoices(invoice_list):
    formatted_invoices = []

    for invoice in invoice_list:
        parts = re.split(r'\s+', invoice)
        expanded = []
        prefix = ""
        for part in parts:
            if part.startswith("FAC"):
                if "-" in part:
                    expanded.extend(expand_range(part))
                else:
                    formatted_part = format_single_invoice(part)
                    prefix = formatted_part[:7]  # Extracting the common prefix
                    expanded.append(formatted_part)
            else:
                if prefix:
                    expanded.append(f"{prefix[:4]}{int(part):05d}")

        formatted_invoices.extend(expanded)

    return formatted_invoices

def expand_range(invoice):
    expanded_invoices = []
    # Split the range into individual parts
    range_parts = re.split(r'[-\s]', invoice)
    prefix = range_parts[0][:4]
    base_number = int(range_parts[0][4:])
    for part in range_parts:
        if part.startswith("FAC"):
            number = int(part[4:])
        else:
            number = base_number + int(part)
        expanded_invoices.append(f"{prefix}{number:06d}")
        base_number += 1

    return expanded_invoices
def format_single_invoice(invoice):
    if "FAC-" in invoice:
        return invoice
    else:
        number = int(invoice.replace("FAC", "").replace("-", ""))
        return f"FAC-{number:06d}"
# Example usage
invoice_list = [
    "FAC-230454",
    "FAC230437  FAC230438",
    "FAC-230446 FAC-230447",
    "FAC-230444  FAC-230445",
    "FAC60-61-62-63-64-65-66",
    "FAC-230435 FAC230439",
    "FAC-230428",
    "FAC-230427",
    "FAC8374  FAC8375",
    "FAC-230424",
    "FAC-230423",
    "FAC-230414",
    "FAC-230415",
    "FAC230406  FAC230407",
    "FAC-230408",
    "FAC-230403",
    "FAC-230397",
    "FAC-230396",
    "FAC-230394",
    "FAC-230393",
    "FAC-230392",
    "FAC-230390 FAC-230391",
    "FAC-230383",
    "FAC-230372  FAC230376",
    "FAC-230368",
    "FAC-230351 FAC230350",
    "FAC240212 213 214 288"  # Your example
]
print("eeeeeee-------------eeeeeeeeeee")
formatted_invoices = format_invoices(invoice_list)
for invoice in formatted_invoices:
    print(invoice)
