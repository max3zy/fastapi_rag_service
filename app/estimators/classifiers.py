# import numpy as np
# from app.estimators.loaders import OnnxLoader
#
#
# class ClassifierRuBert:
#     def __init__(self, loader: OnnxLoader):
#         self.session = loader.session
#         self.tokenizer = loader.tokenizer
#         self.tokenizer_outputs = loader.tokenizer_outputs
#         self.tokenizer_inputs = loader.tokenizer_inputs
#
#     def predict(self, query: str) -> float:
#         encoded_input = self.tokenizer(
#             query, padding=True, truncation=True, return_tensors="np"
#         )
#         output = self.session.run(
#             self.tokenizer_outputs,
#             {
#                 key: val
#                 for key, val in encoded_input.items()
#                 if key in self.tokenizer_inputs
#             },
#         )
#         logits = np.array(output).flatten()
#         score = float(self.softmax(logits)[1])
#         return score
#
#     @staticmethod
#     def softmax(logits: np.ndarray) -> np.ndarray:
#         nominator = np.exp(logits - np.max(logits))
#         divider = np.sum(np.exp(logits - np.max(logits)))
#         return nominator / divider
