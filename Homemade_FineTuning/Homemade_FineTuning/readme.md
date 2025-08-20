## Custom Fine-Tuning with LoRA Adapter on Transformer Model
This project implements a custom fine-tuning pipeline for a transformer-based language model using a LoRA (Low-Rank Adaptation) adapter. The main goal was to adapt a pretrained model efficiently on a specific dataset with a custom dataloader, preprocessing, and training loop.

## Dataset Preprocessing & Dataloader
Loaded the raw dataset and preprocessed it into sequences suitable for language modeling.

Each data sample is transformed into input sequences (x), target sequences (y), and a corresponding mask.

The mask is used to ignore padding tokens or irrelevant positions during loss computation.

Batched the data into mini-batches for training efficiency.

## Sequence Preparation
For each sample, prepared sequences where:

x represents the input tokens fed to the model.

y is the shifted target sequence, representing the expected next token at each position.

mask indicates valid tokens to be considered in the loss, avoiding padding influence.

## LoRA Adapter Implementation

Created an adapter module based on the LoRA method to inject low-rank updates into the model weights.

The adapter modifies specific weight matrices in the transformer layers by learning low-rank matrices A and B.

This approach significantly reduces the number of trainable parameters and enables efficient fine-tuning on large models.

## Training Loop
Implemented a training loop that:

Loads batches from the dataloader.

Moves inputs, targets, and masks to the device (GPU/CPU).

Runs the model forward pass to obtain logits.

Computes masked cross-entropy loss to focus on relevant tokens only.

Performs backpropagation and gradient clipping to maintain training stability.

Steps the optimizer to update parameters.

Optionally uses mixed precision training (float16) with gradient scaling to avoid NaNs.

Tracks and outputs the running loss for monitoring.