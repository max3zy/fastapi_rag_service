from enum import Enum

# from da_robot_max_chain.da_log.events import event_field

#
# class LoggerEvents(str, Enum):
#     SERVICE_LOAD_MODEL_ERROR = event_field(
#         value="SERVICE_LOAD_MODEL_ERROR",
#         description="Не удалось загрузить всю модель по непонятной причине",
#     )
#
#     TOKENIZER_NOT_FOUND_ERROR = event_field(
#         value="TOKENIZER_NOT_FOUND_ERROR",
#         description="Не обнаружен токенайзер по указанному пути",
#     )
#
#     MODEL_NOT_FOUND_ERROR = event_field(
#         value="MODEL_NOT_FOUND_ERROR",
#         description="Не обнаружена модель по указанному пути",
#     )
#
#     PROVIDER_NOT_FOUND_ERROR = event_field(
#         value="PROVIDER_NOT_FOUND_ERROR",
#         description="Не обнаружен указанный провайдер",
#     )
#
#     SERVICE_LOAD_MODEL_SUCCESS = event_field(
#         value="SERVICE_LOAD_MODEL_SUCCESS",
#         description="Модель и токенайзер успешно загружены",
#     )
#     SERVICE_PREDICT_ERROR = event_field(
#         value="SERVICE_PREDICT_ERROR",
#         description="Ошибка при выполнении предсказания сервиса",
#     )
#     SERVICE_V1_SUCCESS = event_field(
#         value="SERVICE_V1_SUCCESS",
#         description="Эндпоинт v1 сервиса успешно завершил свою работу",
#     )
