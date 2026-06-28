import json
import re
import numpy as np
from pathlib import Path

class Preprocessing:
    def __init__(self):
        # Load MobileBERT vocab dari file
        self.vocab = self.load_vocab()
        self.max_length = 128

    def load_vocab(self):
        """Load vocab dari file txt"""
        vocab_path = Path(__file__).parent / "mobilebert_tokenizer" / "vocab.txt"
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab = [line.strip() for line in f]
        return {word: idx for idx, word in enumerate(vocab)}

    def tokenize_single_sentence(self, text):
        """Tokenize satu kalimat tanpa library transformers"""
        # Lowercase untuk MobileBERT uncased
        text = text.lower()

        # Tokenisasi sederhana (split kata dan tanda baca)
        tokens = []
        # Cari kata dan tanda baca
        for match in re.finditer(r'\w+|[^\w\s]', text):
            token = match.group()
            tokens.append(token)

        # Convert ke token IDs
        input_ids = []
        for token in tokens:
            if token in self.vocab:
                input_ids.append(self.vocab[token])
            else:
                # Subword tokenization sederhana (fallback ke [UNK])
                # Untuk akurasi lebih baik, bisa implement BPE di sini
                input_ids.append(self.vocab.get('[UNK]', 100))

        # Format BERT: [CLS] + tokens + [SEP]
        cls_id = self.vocab.get('[CLS]', 101)
        sep_id = self.vocab.get('[SEP]', 102)
        pad_id = self.vocab.get('[PAD]', 0)

        input_ids = [cls_id] + input_ids + [sep_id]

        # Padding atau truncation
        if len(input_ids) > self.max_length:
            input_ids = input_ids[:self.max_length]
            input_ids[-1] = sep_id  # Pastikan token terakhir adalah [SEP]
        else:
            input_ids = input_ids + [pad_id] * (self.max_length - len(input_ids))

        # Attention mask (1 untuk token real, 0 untuk padding)
        attention_mask = [1] * min(len(input_ids), self.max_length)
        attention_mask = attention_mask + [0] * (self.max_length - len(attention_mask))

        # Token type ids (semua 0 untuk single sentence)
        token_type_ids = [0] * self.max_length

        return {
            'input_ids': np.array([input_ids], dtype=np.int64),
            'attention_mask': np.array([attention_mask], dtype=np.int64),
            'token_type_ids': np.array([token_type_ids], dtype=np.int64)
        }

    def split_sentences(self, text):
        """Memecah teks menjadi list kalimat"""
        # Pisahkan berdasarkan . ! ? diikuti spasi atau akhir string
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def text_cleaning(self, text):
        """Bersihkan teks"""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_pdf_direct(pdf_path):
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            text = "\n".join([page.extract_text() for page in reader.pages])
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"