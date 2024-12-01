# import os
# from os.path import exists
#
# from da_robot_max_chain.da_log.logger import logger_factory
# from onnxruntime import (
#     GraphOptimizationLevel,
#     InferenceSession,
#     SessionOptions,
#     get_all_providers,
# )
# from transformers import BertTokenizerFast
#
# from app.da_log.events import LoggerEvents
# from app.da_log.logger import LogExtra
# from app.utils.exceptions import (
#     ModelNotFoundException,
#     ProviderNotFoundException,
#     TokenizerNotFoundException,
# )
# from app.utils.types import ComputeProvider
#
# logger = logger_factory(__name__)
#
#
# class OnnxLoader:
#     tokenizer = None
#     tokenizer_folder_name = "tokenizer"
#     session = None
#     tokenizer_inputs = {}
#     tokenizer_outputs = []
#
#     def __init__(
#         self,
#         path_to_models: str,
#         classifier_model: str,
#         provider: str = ComputeProvider.CPUExecutionProvider,
#         core_count: int = 1,
#     ):
#         self.provider = provider
#         self.core_count = core_count
#         self.load_from_artifacts(
#             path_to_models=path_to_models, classifier_model=classifier_model
#         )
#         logger.info(
#             "Модель и токенайзер успешно загружены",
#             extra=LogExtra(
#                 path_to_models=path_to_models,
#                 classifier_model=classifier_model,
#                 event=LoggerEvents.SERVICE_LOAD_MODEL_SUCCESS,
#             ).dict(),
#         )
#
#     def load_from_artifacts(self, path_to_models: str, classifier_model: str):
#         try:
#             self.tokenizer = self.load_tokenizer(path_to_models)
#             self.session = self.load_model(path_to_models, classifier_model)
#             self.tokenizer_inputs = {
#                 inp.name for inp in self.session.get_inputs()
#             }
#             self.tokenizer_outputs = [
#                 out.name for out in self.session.get_outputs()
#             ]
#         except ModelNotFoundException as exp:
#             logger.exception(
#                 exp,
#                 extra=LogExtra(
#                     path_to_models=path_to_models,
#                     classifier_model=classifier_model,
#                     event=LoggerEvents.MODEL_NOT_FOUND_ERROR,
#                 ).dict(),
#             )
#             raise exp
#         except TokenizerNotFoundException as exp:
#             logger.exception(
#                 exp,
#                 extra=LogExtra(
#                     path_to_models=path_to_models,
#                     classifier_model=classifier_model,
#                     event=LoggerEvents.TOKENIZER_NOT_FOUND_ERROR,
#                 ).dict(),
#             )
#             raise exp
#         except ProviderNotFoundException as exp:
#             logger.exception(
#                 exp,
#                 extra=LogExtra(
#                     path_to_models=path_to_models,
#                     classifier_model=classifier_model,
#                     event=LoggerEvents.PROVIDER_NOT_FOUND_ERROR,
#                 ).dict(),
#             )
#             raise exp
#         except Exception as exp:
#             logger.exception(
#                 exp,
#                 extra=LogExtra(
#                     path_to_models=path_to_models,
#                     classifier_model=classifier_model,
#                     event=LoggerEvents.SERVICE_LOAD_MODEL_ERROR,
#                 ).dict(),
#             )
#             raise exp
#
#     def load_model(
#         self, path_to_models: str, classifier_model: str
#     ) -> InferenceSession:
#         if self.provider not in get_all_providers():
#             raise ProviderNotFoundException(
#                 (
#                     "Указанный провайдер {provider} "
#                     "не обнаружен среди доступных: {all_providers}"
#                 ).format(
#                     provider=self.provider, all_providers=get_all_providers()
#                 )
#             )
#
#         model_path = os.path.join(path_to_models, classifier_model)
#         if not exists(model_path):
#             raise ModelNotFoundException(
#                 (
#                     "По указанному пути {model_path} " "модель не обнаружена!"
#                 ).format(model_path=model_path)
#             )
#         options = SessionOptions()
#         options.intra_op_num_threads = self.core_count
#         options.graph_optimization_level = (
#             GraphOptimizationLevel.ORT_ENABLE_ALL
#         )
#         session = InferenceSession(
#             model_path, options, providers=[self.provider]
#         )
#
#         session.disable_fallback()
#         return session
#
#     def load_tokenizer(self, path_to_models: str) -> BertTokenizerFast:
#         tokenizer_path = os.path.join(path_to_models, self.tokenizer_folder_name)
#         if not exists(tokenizer_path) or os.listdir(tokenizer_path) == 0:
#             raise TokenizerNotFoundException(
#                 (
#                     "По указанному пути {tokenizer_path} "
#                     "токенайзер не обнаружен!"
#                 ).format(tokenizer_path=tokenizer_path)
#             )
#
#         tokenizer = BertTokenizerFast.from_pretrained(
#             tokenizer_path, local_files_only=True
#         )
#         return tokenizer
