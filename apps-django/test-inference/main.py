from preprocessing import Preprocessing
from model import MobileBert
from SummaryGenerator import SummaryGenerator
dokumen = r'D:\Kuliah\Pijak Capstone\inference\teks_contoh.pdf'
model_path = r'D:\Kuliah\Pijak Capstone\inference\model.onnx'

preprocessing = Preprocessing()
mobilebert = MobileBert(
    path_model=model_path,
    inputs=None
)

summary_generator = SummaryGenerator(
    preprocessing=preprocessing,
    model=mobilebert,
    compression_ratio=0.27
)

summary = summary_generator.generate_summary(dokumen)

print(summary)
