# Invoice Data Extractor

A small human-in-the-loop system for pulling structured data out of PDF invoices. You label invoices in a Streamlit app by clicking on the words in the PDF, the labels become training data, and a LayoutLMv3 model learns to find the same fields on new invoices by itself.

The idea behind it: instead of annotating a big dataset up front, the people who already type invoice data into a spreadsheet do their normal work in the tool. Every invoice they process adds to the training data, and once the model is good enough it suggests the values and the person only checks them.

## What's in the repo

```
app/
  invoice_processor.py        Streamlit annotation app
  invoice_processing/         PDF reading, click-to-label UI, CSV and JSON handling
  machine_learning/
    separated/                one model setup: data cleaning, training, evaluation, inference
    united/                   second setup: same steps, labels structured differently
  state/, handlers/           session state and a helper that creates an empty results CSV
tests/                        notebooks used while training and testing inference
src/                          package stub
```

## How it works

1. **Upload a PDF.** The words and their positions are read from the PDF's text layer with PyMuPDF, and the page is shown with a box around each word. This means it works on PDFs that contain real text, not on scanned images.
2. **Click to label.** Pick a field and click the words that make it up. The fields are the columns in `COLUMNS` in `app/invoice_processing/user_data_handling/csv_handling.py` (invoice number, dates, issuer, receiver, VAT, totals, line items and two free `custom_field` columns). Rename or replace them to fit your own invoices. The result goes into a CSV row, and the word-level labels go into JSON.
3. **Train.** The labelled JSON is cleaned and turned into a dataset, then `microsoft/layoutlmv3-base` is fine-tuned for token classification (`*_data_cleaning.py`, then `*_model_training.py`).
4. **Evaluate and predict.** `*_model_evaluation.py` scores the model on a held-out set, and the `*_inference.py` scripts run it on a new invoice.

## Running it

You need Python 3.11 or newer.

```bash
pip install -e .

# one-time setup, from the repo root
mkdir -p app/data/annotated_data/csvs app/data/annotated_data/jsons
python app/handlers/csv_hard_reset.py
PYTHONPATH=app python -c "from invoice_processing.user_data_handling.json_handling import json_creation; json_creation()"

streamlit run app/invoice_processor.py
```

Run everything from the repo root, because the file paths in the code are relative to it. Training uses PyTorch and is much faster on a GPU. The notebooks in `tests/` show a training and inference run; point the `pdf_path` in them at one of your own invoices.

## What is not included

No invoices, annotations or trained models are in this repo. The file types that could hold them (`*.pdf`, `*.csv`, `*.json`, images, model files) and the `app/data/` folder are in `.gitignore`. To try it you need your own invoices and your own labels. Only use invoices you are allowed to process.

## Status

A working prototype and a learning project. The training scripts and notebooks are rough, there are no automated tests, and some scripts contain commented-out experiments.

## Stack

Python, Streamlit, PyMuPDF, Hugging Face Transformers and Datasets (LayoutLMv3), PyTorch, scikit-learn, seqeval.
