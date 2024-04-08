from transformers import AutoTokenizer, BertTokenizer, BertForSequenceClassification, RobertaForSequenceClassification, RobertaTokenizer, AutoModelForSequenceClassification

# Save the model 
def save_model_x():
    # Define the model
    task='sentiment'
    model_name = f"cardiffnlp/twitter-roberta-base-{task}"

    # Load model and tokenizer from Hugging Face
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Define your local directory path where you want to save the model and tokenizer
    local_dir = '/root/models/x_model'

    # Save model and tokenizer locally
    model.save_pretrained(local_dir)
    tokenizer.save_pretrained(local_dir)


def save_model_x2():
    # Define the model
    task='sentiment'
    model_name = f"cardiffnlp/twitter-roberta-base-sentiment-latest"

    # Load model and tokenizer from Hugging Face
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Define your local directory path where you want to save the model and tokenizer
    local_dir = '/root/models/x2_model'

    # Save model and tokenizer locally
    model.save_pretrained(local_dir)
    tokenizer.save_pretrained(local_dir)



def save_model_xi():
    # Define the model
    task='irony'
    model_name = f"cardiffnlp/twitter-roberta-base-{task}"

    # Load model and tokenizer from Hugging Face
    model = RobertaForSequenceClassification.from_pretrained(model_name)
    tokenizer = RobertaTokenizer.from_pretrained(model_name)

    # Define your local directory path where you want to save the model and tokenizer
    local_dir = '/root/models/xi_model'

    # Save model and tokenizer locally
    model.save_pretrained(local_dir)
    tokenizer.save_pretrained(local_dir)

def save_model_fbtone():
    model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
    
    # Define your local directory path where you want to save the model and tokenizer
    local_dir = '/root/models/fbtone_model'

    # Save model and tokenizer locally
    model.save_pretrained(local_dir) 
    tokenizer.save_pretrained(local_dir)

def save_model_lenglish():
    model = RobertaForSequenceClassification.from_pretrained("siebert/sentiment-roberta-large-english")
    tokenizer = RobertaTokenizer.from_pretrained("siebert/sentiment-roberta-large-english")
    
    # Define your local directory path where you want to save the model and tokenizer
    local_dir = '/root/models/lengish_model'

    # Save model and tokenizer locally
    model.save_pretrained(local_dir) 
    tokenizer.save_pretrained(local_dir)

save_model_fbtone()
#save_model_lenglish()
#save_model_x()
#save_model_x2()
#save_model_xi()
