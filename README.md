# My Homemade Fine-Tuning with LoRA

This project is my **from-scratch reimplementation of a LoRA (Low-Rank Adaptation) fine-tuning pipeline**.
Unlike standard workflows that rely on high-level APIs (e.g. `peft`, `LoRAConfig`, or `safetensors` integrations), this repository is built **entirely by hand**, step by step:

- **Custom preprocessing pipeline** for the dataset.
- **Handwritten adapter layers** implementing the LoRA decomposition (`W ≈ W₀ + A·B`) without shortcuts.
- **Custom training loop** — no Trainer API, no Hugging Face abstractions.

The goal of this project is **learning by reimplementing**, ensuring that every matrix multiplication, gradient flow, and weight update is fully transparent and under control.

---

##  Features

- **LoRA Layers from scratch**
  - Manual definition of adapter layers `A` and `B`.
  - Clear separation between frozen base weights and trainable low-rank adapters.
  - PyTorch implementation with explicit forward passes.

- **Custom Preprocessing**
  - Tokenization and dataset preparation tailored for the experiment.
  - No reliance on `datasets` high-level APIs — everything handled explicitly.

- **Custom Training Loop**
  - Explicit `forward`, `loss.backward()`, and `optimizer.step()` calls.
  - Full control over batching, gradient accumulation, and checkpointing.
  - Logging of loss & performance without external training wrappers.

---

##  Project Structure