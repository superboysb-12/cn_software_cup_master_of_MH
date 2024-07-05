import requests
import base64
import torch
from transformers import BertTokenizer, BertModel
from torch import nn
import tldextract

def get_main_domain(url):
    ext = tldextract.extract(url)
    main_domain = ext.registered_domain
    return main_domain


def get_url_id(url):
    url_bytes = url.encode("utf-8")
    url_id = base64.urlsafe_b64encode(url_bytes).decode().strip("=")
    return url_id

def check_url_with_api(url):
    headers = {
        "x-apikey": "c0d7ffa4bb65e8b388580fed496e8ae443edb8ebab4e551fe348e9442faa3ce4"
    }

    url=get_main_domain(url)
    url_id = get_url_id(url)

    url_report_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    response = requests.get(url_report_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None





class BertClassifier(nn.Module):
    def __init__(self, dropout=0.5):
        super(BertClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 5)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)
        return final_layer


class url_check:
    def __init__(self, checkpoint_path='checkpoint_epoch_4.pth'):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertClassifier()
        self.state_dict = torch.load(checkpoint_path)

        self.state_dict = {k: v for k, v in self.state_dict.items() if k in self.model.state_dict()}

        self.model.load_state_dict(self.state_dict, strict=False)

        self.model.eval()

        use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if use_cuda else "cpu")
        if use_cuda:
            self.model = self.model.cuda()

    def predict(self, text):
        text=get_main_domain(text)
        encoding = self.tokenizer(text, padding='max_length', max_length=64, truncation=True, return_tensors="pt")
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            output = self.model(input_ids, attention_mask)

        predicted_class = output.argmax(dim=1).item()
        return predicted_class

