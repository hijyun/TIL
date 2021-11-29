# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + id="zd1BTOAoNVYn"
# %%capture
# !pip install nlp==0.4.0
# !pip install transformers==3.5.1

# + colab={"base_uri": "https://localhost:8080/"} id="4__IhOV4Nzwq" executionInfo={"status": "ok", "timestamp": 1637717888042, "user_tz": -540, "elapsed": 3460, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="68405832-cce5-4fc3-e984-fb6e1985e242"
# !pip3 install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html

# + id="EzuzR4orNZes"
from transformers import BertForSequenceClassification, BertTokenizerFast, Trainer, TrainingArguments
from nlp import load_dataset
import torch
import numpy as np

# + colab={"base_uri": "https://localhost:8080/"} id="w7K6M9iNNdIu" executionInfo={"status": "ok", "timestamp": 1637717898888, "user_tz": -540, "elapsed": 2270, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="2f004070-8f08-435c-d43f-dcf66d5814a4"
# !gdown https://drive.google.com/uc?id=11_M4ootuT7I1G0RlihcC0cA3Elqotlc-
dataset = load_dataset('csv', data_files='./imdbs.csv', split='train')

# + colab={"base_uri": "https://localhost:8080/", "height": 81, "referenced_widgets": ["7f4b660ceaa2479b860ded1855c5f292", "c73b284c692945688c546fdca9b7e9f1", "6431a4b0058b4599bd57b6dbd11f4d73", "bf4340d00f1e42428651df53b3f12ff2", "e9fc670eb7dd43cd866344fa83b03fd5", "faaa079e660e4752a6ec6118b02e8fd3", "7dfc1ac07d3344419165214d3888c1d7", "54ae4d84ac97432ea88ebf3dcdc3dfe6", "bc1c204927d34b10a0051f09f091bbd0", "1534651743574d4d86450e494da51b2e", "dfebcb71d3004b988318120977fdfcfd", "505f5d8b1913428da5772fe00ed04e47", "bd8abd0fbfda49ccb69c15e86db57054", "ec3176ada13342449e7b8ceca8bbc7e1", "e7c7a968b61c4121a073c77264289692", "d75c4bbfd9834907a98a0810cb458dd5", "fe7509b429a44bbd8b7534c420674283", "bde317580be04c548ac4ef0628846d3b", "4b2ce001ab0348739f3d103b264dd987", "e6eeb4c7bcb643caa6eada988eb4f1c1", "698e2a9bfcca413785d25a891a7653c8", "7951f46d33ff4a37b68a2769f62cd228"]} id="anUZ41DHO3JA" executionInfo={"status": "ok", "timestamp": 1637715106865, "user_tz": -540, "elapsed": 286, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="1322bc58-e85c-4477-bc73-a89c415d691a"
dataset = dataset.train_test_split(test_size=0.3)

# + colab={"base_uri": "https://localhost:8080/"} id="ariND0y6O9Sw" executionInfo={"status": "ok", "timestamp": 1637715110499, "user_tz": -540, "elapsed": 604, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="1c9ad9eb-b64d-4a41-9875-da84d28dd381"
dataset

# + id="_jlqypJ_PBfZ"
train_set = dataset['train']
test_set = dataset['test']

# + colab={"base_uri": "https://localhost:8080/", "height": 193, "referenced_widgets": ["fb9aee274cca4906b14d85c0d844e51f", "80eac471205f4fc2a8ac2db8e4478dc0", "732381bdbe1548a0a8b8cd639f48041c", "b1255d3e919d4c2fbb1f4448f9d1c0ba", "f24272ce509149beb3155bc64a651787", "277bc64239304e7dbd340a47f79ae166", "8eaad30079314bcdb1a3b1451bea211a", "b47bb748d9a34a90a292d1863b66a09a", "77825c17732c41e996790ce0efc2c1e9", "6194efcbe43e4df983907e627de139a3", "db5968cc1289492c839216be981cb930", "63b2e02d913c4cd0a49b949d16dc30b3", "f7d64f0d2dae48ddaaefe415b232b869", "10d9a00460fd497d83a6c187345d634e", "03dc5bc9e920442fa3d82eb27d484eb3", "8d16245c1fc8403ea107ed638ba537fd", "6c063466650d476598c783773862f153", "18f02f7fb8f9416eade03cf12ab1f39f", "54b057e78b8e48298df515334a78e627", "bc46b478dd1545c6a4d9ddcddf69c6f8", "9c1388057c7842d191ee647398d2491d", "1c51ee78823c483abbd510dcb613f264"]} id="8s3xg7aVPENi" executionInfo={"status": "ok", "timestamp": 1637715129532, "user_tz": -540, "elapsed": 14500, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="08073745-1484-4030-f231-b7f4a963a8ad"
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# + colab={"base_uri": "https://localhost:8080/", "height": 81, "referenced_widgets": ["1baabb97c466458a945217c22098fe4b", "6b61302c6d154ed39fde77131f994b51", "6242f1c4a8904ccfbf82edb0e391e2fb", "6021a67d24764cb58f1da119ed09f9ed", "d2ce288581a1477fb46e865147cff6e5", "254d944d757a46a495a59bb6c85cf3e4", "79c5bd361a674ef28274b94ec2bcf48d", "b290537a8a8f4ed09b18e6e23e8a0942", "c5c59cc2b8e04ec4ba3ad1ba6e88afff", "1f2cf67dc6b842e58636649de3b50727", "cabb18d2e150456b8a729cdcd0938d88", "3124ef8e2ab24062a8f57e12ab5e9f15", "139b64d2ba074021aecf49e8eb05356c", "370ec2e7da00460784a98fd86843db32", "eb37f2384d0b4971b33abd62e6481e0a", "8cf552f8bfc34c59a40e4673b3e2293f", "6cd7fb32fd4a4e55af977d825366a3ab", "fc4b79fd9ea14e4dad27fc84fed879fc", "9c0c1b21a75548039e15cc604369c873", "053de0e181af4b32905aa4dafbb0129e", "dd2efb35fd1740749f74293f868ed771", "c4568ace6de6429c95d443d6b2b00f2a"]} id="IO6mzuIBPHgh" executionInfo={"status": "ok", "timestamp": 1637715132823, "user_tz": -540, "elapsed": 678, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="c5e63877-aee8-4f36-e5f1-a4f5ce75153d"
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

# + colab={"base_uri": "https://localhost:8080/"} id="YvHATaDoPQjr" executionInfo={"status": "ok", "timestamp": 1637715135881, "user_tz": -540, "elapsed": 275, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="e6e381bb-7660-42eb-9257-713cf332045a"
tokenizer('I love Paris')

# + colab={"base_uri": "https://localhost:8080/"} id="an-TR-flPUTQ" executionInfo={"status": "ok", "timestamp": 1637715138269, "user_tz": -540, "elapsed": 288, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="d9161c96-fbbc-4831-9ae5-77ee8f6cc5e0"
tokenizer(['I love Paris', 'birds fly','snow fall'], padding = True, max_length=5)


# + id="30aPJ91NPXWh"
def preprocess(data):
    return tokenizer(data['text'], padding=True, truncation=True)


# + colab={"base_uri": "https://localhost:8080/", "height": 81, "referenced_widgets": ["981704d3342b4d0d82264a56a44f2b11", "13d21152250848caa85ab5154344e233", "8b0868a84695485baeaf4e09754c758d", "8e970eb546644fdda3a6e2e79e589ecf", "972c74270b3447b1a2cd63dee57cbccb", "db5eb9b31bc348cf919954a470d1ce69", "bce4274742fd4eb3bd1e219fe6341d35", "c4892ddc2cf84905b2843ff2ed38cdfe", "f49d8b428953401a9e600671497b52b6", "bc938bcc947042ffae48a375f782c42e", "3f425a2588f64f86b33aae2a6e1055b7", "342f5ebc2c754c04befd54c7ec5b1c96", "040990fa46264bc9af1c16179ab5dc9f", "693836c713fb429cb2c4eb8e647e2492", "7522e84931124cd2b5c45d4a7fed65f7", "597cb4228fcd4ceb8652e542fc22430e", "2cb3c971e239479a92af8f8b11cbe0cb", "4e4ac8054e91416b98228623a58f6461", "b22b239f16a84e2cbf035997bdc8e72a", "a1d36e89a6dd4e7487e2b6afbcb5907d", "2795a53234f24139a1393147ac532e03", "3f2a235327e44e7ea3f66ac13b4b8a28"]} id="AebaaXEaPa4x" executionInfo={"status": "ok", "timestamp": 1637715145318, "user_tz": -540, "elapsed": 460, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="4a17a58a-498a-4476-80ef-4fa361768b92"
train_set = train_set.map(preprocess, batched=True, batch_size=len(train_set))
test_set = test_set.map(preprocess, batched=True, batch_size=len(test_set))

# + id="vsUYLgUVPd69"
train_set.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])
test_set.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])

# + id="hoOgoxDgPjhS"
batch_size = 8
epochs = 2

# + id="4_WtSu9QPkT6"
warmup_steps = 500
weight_decay = 0.01

# + colab={"base_uri": "https://localhost:8080/"} id="1I5ntL_HPmzo" executionInfo={"status": "ok", "timestamp": 1637715157232, "user_tz": -540, "elapsed": 268, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="c9b74c0f-0fd4-4bbc-953e-d532f28ebcc5"
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=epochs,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    warmup_steps=warmup_steps,
    weight_decay=weight_decay,
    evaluate_during_training=True,
    logging_dir='./logs',
)

# + id="XFgWwJF7PpcB"
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_set,
    eval_dataset=test_set
)

# + colab={"base_uri": "https://localhost:8080/", "height": 94} id="YfywNieEPsIR" executionInfo={"status": "ok", "timestamp": 1637715938759, "user_tz": -540, "elapsed": 772885, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="9bd83f2b-2456-4576-ca75-7ce66d7ffdcd"
trainer.train()

# + colab={"base_uri": "https://localhost:8080/", "height": 56} id="JSXd_genPugK" executionInfo={"status": "ok", "timestamp": 1637716319273, "user_tz": -540, "elapsed": 50391, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="f05f5399-4df4-4e9d-e3f1-c892b61da8ca"
trainer.evaluate()

# + id="lr9-3Ky4PxBr"

