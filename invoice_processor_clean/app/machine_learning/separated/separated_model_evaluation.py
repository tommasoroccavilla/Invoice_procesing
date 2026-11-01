import torch
from transformers import Trainer
from sklearn.metrics import classification_report

from separated_data_cleaning import structuring_for_layout_lmv3

from collections import Counter
import numpy as np
from torch import nn


model_path = (
    "app/machine_learning/separated/layoutlmv3-invoice-model-separated-training_args"
)

train_dataset, eval_dataset, model, processor = structuring_for_layout_lmv3()

from transformers import (
    AutoModelForTokenClassification,
)

from transformers import (
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)


model = AutoModelForTokenClassification.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


id2label = model.config.id2label

training_args = TrainingArguments(
    output_dir="./layoutlmv3-invoice-model",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    learning_rate=5e-5,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    save_total_limit=2,
    report_to="none",
    seed=42,
)


def calculate_class_weights(train_dataset, num_labels):
    label_counts = torch.zeros(num_labels)

    for item in train_dataset:
        labels = item["labels"]
        for label in labels:
            if label != -100:
                label_counts[label] += 1

    total = label_counts.sum()
    class_weights = total / (num_labels * label_counts)

    class_weights[0] = class_weights[0] * 0.1

    return class_weights


class WeightedTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(
        self, model, inputs, return_outputs=False, num_items_in_batch=None
    ):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits

        # Apply class weights
        loss_fct = nn.CrossEntropyLoss(weight=self.class_weights.to(logits.device))
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))

        return (loss, outputs) if return_outputs else loss


class_weights = calculate_class_weights(train_dataset, model.config.num_labels)


trainer = WeightedTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    class_weights=class_weights,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)


# print(f"Model loaded from {model_path} and moved to {device}")

# Evaluate on the test set
eval_results = trainer.evaluate(eval_dataset)


print("=== QUANTITATIVE EVALUATION ===")
print(f"Final Validation Loss: {eval_results['eval_loss']:.4f}")

# Get predictions on the test set
predictions = trainer.predict(eval_dataset)
predicted_labels = np.argmax(predictions.predictions, axis=2)
true_labels = predictions.label_ids

# Flatten the arrays for analysis
flat_true_labels = true_labels.flatten()
flat_predictions = predicted_labels.flatten()

# Filter out padding tokens (usually label = -100)
mask = flat_true_labels != -100
flat_true_labels = flat_true_labels[mask]
flat_predictions = flat_predictions[mask]

# Get the unique labels that actually appear in your test set
unique_labels_present = np.unique(flat_true_labels)
present_label_names = [id2label[label_id] for label_id in unique_labels_present]

num_labels = len(model.config.id2label)
target_names = [model.config.id2label[i] for i in range(num_labels)]

# Now use only the labels that actually exist
print("\n=== CLASSIFICATION REPORT (Only Present Labels) ===")
print(
    classification_report(
        flat_true_labels,
        flat_predictions,
        labels=unique_labels_present,
        target_names=present_label_names,
        zero_division=0,
    )
)

# label_counts = Counter(flat_true_labels)
# print("\n=== LABEL DISTRIBUTION ===")
# for label_id, count in label_counts.items():
#     print(f"{id2label[label_id]}: {count} samples")


total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

print(f"Total parameters: {total_params:,}")
print(f"Trainable parameters: {trainable_params:,}")

# Model file size (on disk)
import os

model_file = os.path.join(model_path, "pytorch_model.bin")
if os.path.exists(model_file):
    print(f"Model file size: {os.path.getsize(model_file)/1024**2:.2f} MB")


# from sklearn.metrics import confusion_matrix
# import seaborn as sns
# import matplotlib.pyplot as plt

# cm = confusion_matrix(flat_true_labels, flat_predictions, labels=unique_labels_present)

# plt.figure(figsize=(10,8))
# sns.heatmap(cm, annot=True, fmt="d", xticklabels=present_label_names, yticklabels=present_label_names)
# plt.xlabel("Predicted")
# plt.ylabel("True")
# plt.title("Confusion Matrix")
# plt.show()

# from PIL import Image

# image = Image.open("path/to/your_invoice_page.png").convert("RGB")

# encoding = processor(
#     image, return_tensors="pt", truncation=True, padding="max_length", max_length=512
# )

# with torch.no_grad():
#     outputs = model(**{k: v.to(model.device) for k, v in encoding.items()})

# logits = outputs.logits
# predictions = logits.argmax(-1).squeeze().cpu().numpy()

# tokens = encoding.tokens()
# labels = [id2label[pred] for pred in predictions]

# for word, label in zip(tokens, labels):
#     if word not in [None, "[PAD]", "[CLS]", "[SEP]"]:
#         print(f"{word}: {label}")

# from collections import defaultdict

# entities = defaultdict(list)
# current_entity = None

# for word, label in zip(tokens, labels):
#     if label.startswith("B-"):
#         current_entity = label[2:]
#         entities[current_entity].append(word)
#     elif label.startswith("I-") and current_entity:
#         entities[current_entity].append(word)
#     else:
#         current_entity = None

# # Join tokens into text
# for ent, words in entities.items():
#     print(f"{ent}: {' '.join(words)}")
