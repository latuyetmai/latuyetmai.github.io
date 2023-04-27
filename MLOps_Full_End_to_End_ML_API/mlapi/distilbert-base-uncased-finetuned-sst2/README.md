---
license: apache-2.0
tags:
- generated_from_trainer
datasets:
- glue
metrics:
- accuracy
model-index:
- name: distilbert-base-uncased-finetuned-sst2
  results:
  - task:
      name: Text Classification
      type: text-classification
    dataset:
      name: glue
      type: glue
      config: sst2
      split: train
      args: sst2
    metrics:
    - name: Accuracy
      type: accuracy
      value: 0.9025229357798165
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# distilbert-base-uncased-finetuned-sst2

This model is a fine-tuned version of [distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased) on the glue dataset.
It achieves the following results on the evaluation set:
- Loss: 0.2817
- Accuracy: 0.9025


## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 512
- eval_batch_size: 512
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 5

### Training results

| Training Loss | Epoch | Step | Validation Loss | Accuracy |
|:-------------:|:-----:|:----:|:---------------:|:--------:|
| No log        | 1.0   | 132  | 0.2534          | 0.8956   |
| No log        | 2.0   | 264  | 0.2679          | 0.9002   |
| No log        | 3.0   | 396  | 0.2817          | 0.9025   |
| 0.1896        | 4.0   | 528  | 0.2933          | 0.9002   |
| 0.1896        | 5.0   | 660  | 0.3008          | 0.9002   |


### Framework versions

- Transformers 4.23.1
- Pytorch 1.12.1+cu116
- Datasets 2.6.1
- Tokenizers 0.13.1