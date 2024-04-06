from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import csv
from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification


def x0_model(text):
    local_dir = '/root/models/lengish_model'
    sentiment_analysis = pipeline("sentiment-analysis",model=local_dir)
    return sentiment_analysis(text)


def x1_model(text):
    local_dir = '/root/models/fbtone_model'
    model = BertForSequenceClassification.from_pretrained(local_dir,num_labels=3)
    tokenizer = BertTokenizer.from_pretrained(local_dir)
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp(text)


'''Current Cardiff twitter classification'''
def preprocess_x2(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def x2_model(input_text):
    MODEL = '/root/models/x2_model'
    model_path = MODEL
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    config = AutoConfig.from_pretrained(model_path)
    # PT
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.save_pretrained(model_path)
    processed_text = preprocess_x2(input_text)
    encoded_input = tokenizer(processed_text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    l = config.id2label[ranking[0]]
    return l
        

# Preprocess text (username and link placeholders)
def preprocess_xi(text):
    new_text = [
    ]
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)



def xi_model(input_text):
    MODEL = '/root/models/xi_model'
    MAPPING = '/root/models/xi_model/mapping.txt'
    
    model_path = MODEL
    mapping_path = MAPPING
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # download label mapping
    labels=[]
    with open(mapping_path, 'r') as file:
        csvreader = csv.reader(file, delimiter='\t')
        labels = [row[1] for row in csvreader if len(row) > 1]

    # PT
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    processed_text = preprocess_xi(input_text)
    encoded_input = tokenizer(processed_text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    
    l = labels[ranking[0]]
    s = scores[ranking[0]]
    if l == 'irony' and s > .8:
        return 'irony'
    else:
        return 'non_irony'