# from dataclasses import dataclass
# from enum import Enum
# from typing import Any, Dict, Optional, Union
#
# from pydantic import BaseModel
#
#
# @dataclass
# class ClassifyRequest:
#     query: str
#     is_use_score: bool
#     threshold: float
#
#
#
# class EstimatorIn(BaseModel):
#     query: str
#     num_docs: int
#
#
# @dataclass
# class StrategyIn:
#     query: str
#     classify_score: float
#     debug_info: Optional[Dict[str, Any]] = None
#
#
# @dataclass
# class StrategyOut:
#     query: str
#     classify_score: float
#     debug_info: Optional[Dict[str, Any]] = None
#
#
# class ComputeProvider(str, Enum):
#     TensorrtExecutionProvider = "TensorrtExecutionProvider"
#     CUDAExecutionProvider = "CUDAExecutionProvider"
#     MIGraphXExecutionProvider = "MIGraphXExecutionProvider"
#     ROCMExecutionProvider = "ROCMExecutionProvider"
#     OpenVINOExecutionProvider = "OpenVINOExecutionProvider"
#     DnnlExecutionProvider = "DnnlExecutionProvider"
#     TvmExecutionProvider = "TvmExecutionProvider"
#     VitisAIExecutionProvider = "VitisAIExecutionProvider"
#     QNNExecutionProvider = "QNNExecutionProvider"
#     NnapiExecutionProvider = "NnapiExecutionProvider"
#     JsExecutionProvider = "JsExecutionProvider"
#     CoreMLExecutionProvider = "CoreMLExecutionProvider"
#     ArmNNExecutionProvider = "ArmNNExecutionProvider"
#     ACLExecutionProvider = "ACLExecutionProvider"
#     DmlExecutionProvider = "DmlExecutionProvider"
#     RknpuExecutionProvider = "RknpuExecutionProvider"
#     WebNNExecutionProvider = "WebNNExecutionProvider"
#     XnnpackExecutionProvider = "XnnpackExecutionProvider"
#     CANNExecutionProvider = "CANNExecutionProvider"
#     AzureExecutionProvider = "AzureExecutionProvider"
#     CPUExecutionProvider = "CPUExecutionProvider"
