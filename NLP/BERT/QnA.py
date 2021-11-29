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

# + id="IchitnPWmSs_"
# %%capture
# !pip install transformers==3.5.1
# !pip install nlp==0.4.0

# + colab={"base_uri": "https://localhost:8080/"} id="tz0asfPjmsTi" executionInfo={"status": "ok", "timestamp": 1637718302244, "user_tz": -540, "elapsed": 178873, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="df300197-7039-4ac6-f1a9-5473e04ac156"
# !pip3 install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html

# + id="N1hB8UhPnDOp"
import torch
from transformers import BertForQuestionAnswering, BertTokenizer

# + colab={"base_uri": "https://localhost:8080/", "height": 81, "referenced_widgets": ["1d43c495ec8b4ee48fddc8b9a44c31b1", "ce4897d742d84f5a80fb9c346fecb69d", "e050503506f5463990ea7ae87e4de1c3", "8cbd81d778ca42d29e5b382c1d85221d", "6a665c379c1040e8807a89ac728c0d9d", "7ed542fe705843dd9897f1337d727ff7", "ad81af0299e54b9da7b88f17ad29fe15", "a97a29b6afb14b27a681a80b3844f515", "cb984f4595314c86b9e1ebdccc5617aa", "22e22ecf06384ae9bc8295c818307c21", "e103555a360243338376089acb030ec0", "aa2445ac4fa74ca6b5d80128958c5d1a", "b70b263c99fc403e8348b26628ff7305", "1ad42d7b3ffb4193834ceaa5530dea43", "35c98d028b75443b9c30fb70bb1a20a2", "7acccdd1b6174fe2bb4c1f75c2c23fa1", "2f44917e11c848a6a9ed6a475b2ecd99", "36b422d153c141b9bb5609e582279e1c", "0409197ed457404d8cdcc8886d45133f", "db0ac95ba9e3447b903c6489e45d6bbf", "a4c13356b93f43b2bbe1dfd7d8306916", "52689e91db5340bca4259e6046fe5a97"]} id="j8ZvBJKkn_aP" executionInfo={"status": "ok", "timestamp": 1637718467799, "user_tz": -540, "elapsed": 42460, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="2763216e-23b9-4b59-8a7a-49a52df946c1"
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# + colab={"base_uri": "https://localhost:8080/", "height": 49, "referenced_widgets": ["ed3fd09d1faa47cfa36bbde683893a58", "72abe496c56647bfae2e5929b6bc7f6e", "f102d54c44784fedaf80b38a02808055", "3b7bb87905234da7bd3108d54998c346", "a9380f4b82a44993be028c574a1510de", "acd8b3211c9a4483bf2d21dd0e10e61c", "6bf0c8f9c3c9437297dcefa942763984", "2c6b56f309e448fc8f045999d8781226", "77969a8a6f4643dfa72ec96d9eb652d0", "31164ea341184cc98947088daeb44e81", "47493560aed847c1a9e759a759b434da"]} id="teLIT_LhoAbA" executionInfo={"status": "ok", "timestamp": 1637718475386, "user_tz": -540, "elapsed": 655, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="3acebd15-1eac-47aa-a6c1-3c973b72dd44"
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# + id="Kno4PekQoK6v"
question = "What is the immune system?"
paragraph = "The immune system is a system of many biological structures and processes within an organism that protects against disease. To function properly, an immune system must detect a wide variety of agents, known as pathogens, from viruses to parasitic worms, and distinguish them from the organism's own healthy tissue."

# + id="E2NL5N48oQlm"
question = '[CLS] ' + question + '[SEP]'
paragraph = paragraph + '[SEP]'

# + id="tWBUILKKoV5W"
question_tokens = tokenizer.tokenize(question)
paragraph_tokens = tokenizer.tokenize(paragraph)

# + id="Pa7ummaFoYyo"
tokens = question_tokens + paragraph_tokens 
input_ids = tokenizer.convert_tokens_to_ids(tokens)

# + id="YCgxwcRhodLH"
segment_ids = [0] * len(question_tokens)
segment_ids += [1] * len(paragraph_tokens)

# + id="PXSY-j_Cofhn"
input_ids = torch.tensor([input_ids])
segment_ids = torch.tensor([segment_ids])

# + id="ZuyY5M_BoiNW"
start_scores, end_scores = model(input_ids, token_type_ids = segment_ids)

# + id="7RnZwYHGok_5"
start_index = torch.argmax(start_scores)
end_index = torch.argmax(end_scores)

# + id="BcxFFWoTonSf" colab={"base_uri": "https://localhost:8080/"} executionInfo={"status": "ok", "timestamp": 1637718603643, "user_tz": -540, "elapsed": 275, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="2b5abe13-d140-47d4-fb8f-a9565e8b8993"
print(' '.join(tokens[start_index:end_index+1]))
