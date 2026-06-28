from pypdf import PdfReader
import re
from transformers import MobileBertTokenizer

class Preprocessing:
    def __init__(self):
        pass
        
    def extract_pdf(self, dokumen_path):
        reader = PdfReader(dokumen_path)
        text = "\n".join([page.extract_text() for page in reader.pages])
        return text
    
    def text_cleaning(self, dokumen_path):
        text = self.extract_pdf(dokumen_path)
        text = text.lower()
        clean_text = re.sub(r'<.*?>', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        return clean_text
    
    def split_sentences(self, dokumen_path):
        """
        Memecah paragraf menjadi list perkalimat
        """
        text = self.text_cleaning(dokumen_path)
        sentences = re.split(r'(?<=[.!?])\s+', str(text))
        
        return[
            sentence.strip() for sentence in sentences if sentence.strip()
        ]

    def tokenisasi(self, text):
        tokenizer = MobileBertTokenizer.from_pretrained("google/mobilebert-uncased")
        tokenized = tokenizer(text, padding="max_length", truncation=True, max_length=128, return_tensors="np")
        return tokenized
    
    def inputs(self, tokenize_data):
        inputs = {
            'input_ids': tokenize_data['input_ids'].astype('int64'),
            'attention_mask': tokenize_data['attention_mask'].astype('int64'),
            'token_type_ids': tokenize_data['token_type_ids'].astype('int64'),
        }

        return inputs

