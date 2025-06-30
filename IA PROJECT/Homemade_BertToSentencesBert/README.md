## BERT Reconstruction & Sentence Embedding Fine-Tuning

This project is a personal reconstruction of the BERT architecture, using a pre-trained open-source BERT model as a base. The goal was to understand the internals of BERT, how it handles token-level contextual representations, and then to build a simple Sentence-BERT (SBERT)-like system from scratch.

# What I Did
BERT Reconstruction with Pretrained Weights
I rebuilt the architecture of the original BERT model manually, layer by layer.

To avoid training everything from scratch, I loaded the pretrained weights from the original open-source BERT base model.

I then ran inference on token pairs to observe how they are represented in the embedding space.

# Token-Level Observations
My initial intuition was that semantically similar tokens (like cat and dog) should be close in the embedding space.

But in reality, BERT is trained to capture contextual meaning, not static similarity.

This means that even semantically related tokens may end up far apart, depending on their contextual usage.

# Sentence Embedding & Pooling Head
To move toward Sentence-BERT, I added a simple pooling head:

For each sentence, I took the mean of all token embeddings in the last layer.

This gives a single fixed-size embedding vector for a full sentence.

# Initial Results
At first, sentence embeddings of semantically close sentences (e.g. "How are you?" vs. "How are things?") were not close in space.

This is expected, since the base BERT is not trained for sentence-level similarity.

# Fine-Tuning with Similarity Regression
To improve semantic clustering in sentence space:

I created sentence pairs with known similarity scores.

Then, I fine-tuned the model using an MSELoss (Mean Squared Error Loss):

x = cosine_similarity(embedding1, embedding2)

y = expected similarity score (a float between 0 and 1)

This is a regression task, not classification.

# Result
After fine-tuning:

Semantically similar sentences are now closer in the embedding space.

The model learns to map sentence meanings more effectively using cosine similarity.

# Next Steps


Add more complex pooling strategies (I think to add MLP before the compute of mean).

Evaluate on real benchmarks (STS-B, etc.)
