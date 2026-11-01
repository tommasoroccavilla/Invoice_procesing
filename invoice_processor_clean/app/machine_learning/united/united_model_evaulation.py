import torch
from transformers import Trainer
from seqeval.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)

from united_data_cleaning import structuring_for_layout_lmv3

model_path = "app/machine_learning/separated/layoutlmv3-invoice-model-separated"

train_dataset, eval_dataset, model, processor = structuring_for_layout_lmv3()

from transformers import LayoutLMv3ForTokenClassification, LayoutLMv3Processor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Model loaded from {model_path} and moved to {device}")

trainer = Trainer(model=model)
predictions, labels, _ = trainer.predict(eval_dataset)

preds = predictions.argmax(-1)

id2label = model.config.id2label

true_labels = [[id2label[l] for l in label if l != -100] for label in labels]

predicted_labels = []
for pred, label in zip(preds, labels):
    preds_i = []
    for p, l in zip(pred, label):
        if l != -100:
            preds_i.append(id2label[int(p)])
    predicted_labels.append(preds_i)


print("Evaluation metrics on test set:")
print("F1:", f1_score(true_labels, predicted_labels))
print("Precision:", precision_score(true_labels, predicted_labels))
print("Recall:", recall_score(true_labels, predicted_labels))

print("\nClassification Report:")
print(classification_report(true_labels, predicted_labels))
