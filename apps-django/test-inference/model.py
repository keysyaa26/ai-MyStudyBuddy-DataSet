import onnxruntime as ort

class MobileBert:
    def __init__(self, path_model, inputs):
        self.path_model = path_model
        self.inputs = inputs

    def proses_model(self):
        session = ort.InferenceSession(
            self.path_model,
            providers=["CPUExecutionProvider"]
        )

        outputs = session.run(None, self.inputs)

        return outputs