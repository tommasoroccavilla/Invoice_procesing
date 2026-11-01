from transformers import (
    AutoProcessor,
    LayoutLMv3ForTokenClassification,
    LayoutLMv3Processor,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)

import torch
from torch import nn

from separated_data_cleaning import structuring_for_layout_lmv3


def calculate_class_weights(train_dataset, num_labels):
    label_counts = torch.zeros(num_labels)
    
    for item in train_dataset:
        labels = item['labels']
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
    
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        
        # Apply class weights
        loss_fct = nn.CrossEntropyLoss(weight=self.class_weights.to(logits.device))
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        
        return (loss, outputs) if return_outputs else loss

train_dataset, eval_dataset, model, processor = structuring_for_layout_lmv3()


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Model loaded and moved to: {device}")

class_weights = calculate_class_weights(train_dataset, model.config.num_labels)
print(f"Class weights calculated: {class_weights}")

training_args = TrainingArguments(
    output_dir="app/machine_learning/separated/layoutlmv3-invoice-model-separated-training_args",
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

trainer = WeightedTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    class_weights=class_weights,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)


print("Starting training...")
train_history = trainer.train()
print("Training completed!")


trainer.save_model()
processor.save_pretrained(
    "app/machine_learning/separated/layoutlmv3-invoice-model-separated"
)
print(
    "Model saved to 'app/machine_learning/separated/layoutlmv3-invoice-model-separated'"
)
