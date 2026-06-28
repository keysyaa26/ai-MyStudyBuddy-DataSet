import numpy as np

class SummaryGenerator:

    def __init__(self, preprocessing, model, compression_ratio=0.27):
        self.preprocessing = preprocessing
        self.model = model
        self.compression_ratio = compression_ratio

    def softmax(self, logits):
        exp = np.exp(logits - np.max(logits))
        return exp / exp.sum(axis=-1, keepdims=True)

    def predict_score(self, sentence):
        tokenized = self.preprocessing.tokenisasi(sentence)
        inputs = self.preprocessing.inputs(tokenized)
        self.model.inputs = inputs
        outputs = self.model.proses_model()
        logits = outputs[0]
        probs = self.softmax(logits)

        return float(probs[0][1])
    
    def rank_sentences(self,sentences):
        ranked = []

        for idx, sentence in enumerate(sentences):
            score = self.predict_score(sentence)
            ranked.append({
                "idx": idx,
                "sentence": sentence,
                "score": score
            })

        return ranked
    
    def select_sentences(self, ranked_sentences):

        total_chars = sum(len(item["sentence"]) for item in ranked_sentences)

        target_chars = int(total_chars *self.compression_ratio)

        ranked = sorted(ranked_sentences, key=lambda x: x["score"], reverse=True)

        selected = []

        current_chars = 0

        for item in ranked:
            selected.append(item)
            current_chars += len(item["sentence"])

            if current_chars >= target_chars:
                break

        selected = sorted(selected,key=lambda x: x["idx"])

        return selected
    
    def generate_summary(self, dokumen_path):
        sentences = (self.preprocessing.split_sentences(dokumen_path))
        ranked = self.rank_sentences(sentences)
        selected = self.select_sentences(ranked)

        summary = " ".join(item["sentence"]for item in selected)

        return summary