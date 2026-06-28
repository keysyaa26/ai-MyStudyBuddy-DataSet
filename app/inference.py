import re  
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import AutoTokenizer

MODEL_PATH = "models/onnx_production"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = ORTModelForSeq2SeqLM.from_pretrained(
    MODEL_PATH
)

def clean_text(text: str) -> str:
    """
    Fungsi Preprocessing / Text Cleaning otomatis untuk mencegah glitch format JSON.
    """
    if not text:
        return ""
        
    # 1. Hapus tanda kutip dua ganda (") internal agar tidak memecah struktur JSON/Swagger
    text = text.replace('"', '')
    
    # 2. Hapus emoji dan karakter aneh. Hanya sisakan huruf, angka, spasi, dan tanda baca standar.
    text = re.sub(r'[^\w\s\d.,!?-]', '', text)
    
    # 3. Ubah enter (\n) atau spasi ganda yang berantakan menjadi satu spasi biasa
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def summarize(text):

    cleaned_text = clean_text(text)

    inputs = tokenizer(
        cleaned_text,  
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        **inputs,
        max_length=150,
        min_length=30,
        num_beams=4,
        use_cache=False  
    )

    summary = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return summary