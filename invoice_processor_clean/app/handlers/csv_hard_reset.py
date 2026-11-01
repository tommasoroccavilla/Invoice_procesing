import pandas as pd

COLUMNS = [
    "file_name",
    "invoice_number",
    "invoice_date",
    "issuer_name",
    "issuer_office",
    "receiver_name",
    "receiver_office",
    "line_items",
    "line_item_amounts",
    "vat",
    "total_amount",
    "due_date",
    "period_start",
    "period_end",
    "custom_field_1",
    "custom_field_2",
]

csv_path = "app/data/annotated_data/csvs/extracted_data.csv"


def csv_creation(columns, csv_path):
    empty_csv = pd.DataFrame(columns=columns)
    empty_csv.to_csv(csv_path, index=False)


csv_creation(COLUMNS, csv_path)
