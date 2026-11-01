from transformers import (
    AutoProcessor,
    LayoutLMv3ForTokenClassification,
    LayoutLMv3Processor,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)

import torch

from united_data_cleaning import structuring_for_layout_lmv3

train_dataset, eval_dataset, model, processor = structuring_for_layout_lmv3()


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Model loaded and moved to: {device}")


training_args = TrainingArguments(
    output_dir="app/machine_learning/united/layoutlmv3-invoice-model-united-training_args",
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


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)


print("Starting training...")
train_history = trainer.train()
print("Training completed!")


trainer.save_model()
processor.save_pretrained("app/machine_learning/united/layoutlmv3-invoice-model-united")
print("Model saved to 'app/machine_learning/united/layoutlmv3-invoice-model-united'")
