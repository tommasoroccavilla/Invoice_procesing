from transformers import AutoModelForTokenClassification
from PIL import Image
import fitz
import io
import torch
from transformers import AutoProcessor


pdf_path = "path/to/your_invoice.pdf"

model = AutoModelForTokenClassification.from_pretrained(
    "app/machine_learning/separated/layoutlmv3-invoice-model-separated-training_args"
)

processor = AutoProcessor.from_pretrained(
    "app/machine_learning/separated/layoutlmv3-invoice-model-separated",
    apply_ocr=False,
)


def extract_text_and_bboxes_from_pdf(pdf_path, dpi=200):
    doc = fitz.open(pdf_path)
    page = doc[0]

    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    image = Image.open(io.BytesIO(img_data)).convert("RGB")

    text_dict = page.get_text("words")

    pdf_width = page.rect.width
    pdf_height = page.rect.height

    img_width, img_height = image.size
    scale_x = 1000 / pdf_width
    scale_y = 1000 / pdf_height

    words = []
    bboxes = []

    for i, word in enumerate(text_dict):
        words.append(text_dict[i][4])
        left = int(text_dict[i][0] * scale_x)
        top = int(text_dict[i][1] * scale_y)
        right = int(text_dict[i][2] * scale_x)
        bottom = int(text_dict[i][3] * scale_y)
        bboxes.append([left, top, right, bottom])

    doc.close()
    return words, bboxes, image


words, bboxes, image = extract_text_and_bboxes_from_pdf(pdf_path, dpi=200)
# img_width, img_height = image.size
# print(words, bboxes)

encoding = processor(
    image,
    words,
    boxes=bboxes,
    return_tensors="pt",
    truncation=True,
    padding="max_length",
    max_length=512,
)

model.eval()
with torch.no_grad():
    outputs = model(**encoding)
    logits = outputs.logits

    probs = torch.nn.functional.softmax(logits, dim=-1)

    confidences, predictions = probs.max(dim=-1)
    predictions = predictions.squeeze().tolist()
    confidences = confidences.squeeze().tolist()

token_boxes = encoding.bbox.squeeze().tolist()
is_subword = encoding.sequence_ids()

word_level_predictions = []
word_level_boxes = []
word_level_confidences = []

for idx, (pred, box, conf, seq_id) in enumerate(
    zip(predictions, token_boxes, confidences, is_subword)
):
    if seq_id == 0:
        word_level_predictions.append(pred)
        word_level_boxes.append(box)
        word_level_confidences.append(conf)

id2label = model.config.id2label

print(model.config.id2label)
print(model.config.label2id)

print("=" * 100)
print("ALL PREDICTIONS:")
print("=" * 100)
for word, pred_id, box, conf in zip(
    words[: len(word_level_predictions)],
    word_level_predictions,
    word_level_boxes,
    word_level_confidences,
):
    label = id2label[pred_id]
    print(f"Word: {word:20} | Label: {label:20} | Confidence: {conf:.4f} | Box: {box}")
