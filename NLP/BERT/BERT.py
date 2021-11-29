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

# + id="MxoJFX7uFmiC"
# %%capture
# !pip install transformers==3.5.1

# + colab={"base_uri": "https://localhost:8080/"} id="OH7_I-vYFqDp" executionInfo={"status": "ok", "timestamp": 1637676070484, "user_tz": -540, "elapsed": 180755, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="918a6649-cefc-4b6f-a88b-412575756d59"
# !pip3 install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html

# + id="CEgM_Qr9F5fL"
from transformers import BertModel, BertTokenizer
import torch

# + colab={"base_uri": "https://localhost:8080/", "height": 81, "referenced_widgets": ["e0474d3ccb4046698464c30b49f6e3c2", "d4f6f69d5bd64a4b8e1b933d819d3fb3", "0dd4a457950f4746a8ebbf38c881e70d", "ee346e1122ad477280edf3497f411785", "486ee4c7361242f983f5e7000711532c", "68601084f1b2475184bae63d6264ea82", "82774fd037c34fbe8d89b3b985513ed6", "4450685c4e7f4716a9c64eeb3f7c395c", "8d364ff209f1461f94b6117417704a65", "1f9dc9878fd74c45af5c717f193df342", "0335e9fa42fe4063810102e73dab27f4", "f41c6069d34445ebbcac33811c59fa43", "cf0c1dd954f34025b625b5d25e36231f", "44d2867cd5b44880bbece5bcba080ff2", "ef09d7d18b5c4d8484f2ddb61b9a0f12", "e5984b81655e4212b46e1cf432e67145", "55d50b3d2a934852b05b6a1dc2c2f4d8", "da659ab46087470992ac51b49474f8f9", "6a745377286f4e679febe2312dafb371", "588165f48ae040d3ba13823c2fe8947b", "054840e012074f5dab43d16d66289e3a", "622d9f9fa7074f34b69d1fd0f9fe8c79"]} id="t_E86zovG4JQ" executionInfo={"status": "ok", "timestamp": 1637676252909, "user_tz": -540, "elapsed": 15158, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="c1f50745-de7a-4ec7-f9cd-aafa2b06bed3"
model = BertModel.from_pretrained('bert-base-uncased')

# + colab={"base_uri": "https://localhost:8080/", "height": 49, "referenced_widgets": ["a4c879f5998d45599f234b7c3d42cf9f", "5335dcce7b3e4160b9c2216e8a776fda", "ce8fb235d75c403483c679601ec6d8e4", "69e08a4cff8a4d49a9ea4d2b8a696f13", "225cce4ad19045c993bd4e048fbf40b8", "47165198952d4158a7355833712446b5", "a628915884be40158f3a053cc11274af", "7f0b1b2899254ab38720581b25615650", "7d2658eb88434009b2a00d5108786e14", "af2e89011cf845e5a04c5ae785379e52", "cf93a5f1af394b95b198c7df768fdcd9"]} id="eMVgJ5JNHEoW" executionInfo={"status": "ok", "timestamp": 1637676263428, "user_tz": -540, "elapsed": 1139, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="80d41ed8-8304-4f7d-a128-d40e16920565"
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# + id="iyKVELciHNO-"
sentence = 'I love Paris'

# + id="Eqc-gJFuHQGe"
tokens = tokenizer.tokenize(sentence)

# + colab={"base_uri": "https://localhost:8080/"} id="VqoO8NkwHev2" executionInfo={"status": "ok", "timestamp": 1637677770273, "user_tz": -540, "elapsed": 423, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="856a591e-ed48-45fb-fb51-7fbbf34aafa8"
print(tokens)

# + id="LuuGBrt4HhMi"
tokens = ['[CLS]'] + tokens + ['[SEP]']

# + colab={"base_uri": "https://localhost:8080/"} id="oyOvAF60HnR-" executionInfo={"status": "ok", "timestamp": 1637677773643, "user_tz": -540, "elapsed": 8, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="2ab86ac7-f83d-421b-e13b-cfb091b2a030"
print(tokens)

# + id="q6b4nfemHo6e"
tokens = tokens + ['[PAD]'] + ['[PAD]']

# + colab={"base_uri": "https://localhost:8080/"} id="DeUTM3APHyNG" executionInfo={"status": "ok", "timestamp": 1637677788901, "user_tz": -540, "elapsed": 312, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="d81a8015-223d-46a4-88ce-86f528be3456"
print(tokens)

# + colab={"base_uri": "https://localhost:8080/"} id="G4w-s11CHz-u" executionInfo={"status": "ok", "timestamp": 1637677793852, "user_tz": -540, "elapsed": 354, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="c0ee9a81-f68d-419d-8295-f24c644429a5"
attention_mask = [1 if i!= '[PAD]' else 0 for i in tokens]
print(attention_mask)


# + colab={"base_uri": "https://localhost:8080/"} id="xlC9FWTYIEkt" executionInfo={"status": "ok", "timestamp": 1637677799035, "user_tz": -540, "elapsed": 447, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="18207d38-9665-4426-c884-21dd7b5c7102"
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print(token_ids)

# + id="NYbZBP3bIWTO"
token_ids = torch.tensor(token_ids).unsqueeze(0)
attention_mask = torch.tensor(attention_mask).unsqueeze(0)

# + id="SHdk252HIdqF"
hidden_rep, cls_head = model(token_ids, attention_mask = attention_mask)

# + colab={"base_uri": "https://localhost:8080/"} id="UX8IYTWdIkx0" executionInfo={"status": "ok", "timestamp": 1637677809488, "user_tz": -540, "elapsed": 10, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="48b30065-dbce-4fba-9439-21cc7d01fc4f"
print(hidden_rep.shape)

# + colab={"base_uri": "https://localhost:8080/"} id="G5aaEJ1vIn4l" executionInfo={"status": "ok", "timestamp": 1637677811837, "user_tz": -540, "elapsed": 310, "user": {"displayName": "Hyon Hee Kim", "photoUrl": "https://lh3.googleusercontent.com/a/default-user=s64", "userId": "14896894259665252236"}} outputId="d5cccb81-b1bb-41a1-fbaa-063077422b3d"
print(hidden_rep[0].shape)
