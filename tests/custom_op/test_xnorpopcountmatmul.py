# Copyright (c) 2020, Xilinx
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of FINN nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from pkgutil import get_data

import brevitas.onnx as bo
import numpy as np
import onnx
import onnx.helper as helper
import onnx.numpy_helper as nph
from onnx import TensorProto

import finn.core.onnx_exec as oxe
from finn.core.datatype import DataType
from finn.core.modelwrapper import ModelWrapper
from finn.transformation.bipolar_to_xnor import ConvertBipolarMatMulToXnorPopcount
from finn.transformation.fold_constants import FoldConstants
from finn.transformation.general import GiveReadableTensorNames, GiveUniqueNodeNames
from finn.transformation.infer_datatypes import InferDataTypes
from finn.transformation.infer_shapes import InferShapes
from finn.transformation.streamline.sign_to_thres import ConvertSignToThres
from finn.util.test import get_test_model_trained

export_onnx_path = "test_xnorpopcountmatmul.onnx"


def test_xnorpopcountmatmul():
    M = 1
    K = 3
    N = 3
    x = helper.make_tensor_value_info("x", TensorProto.FLOAT, [M, K])
    W = helper.make_tensor_value_info("W", TensorProto.FLOAT, [K, N])
    out = helper.make_tensor_value_info("out", TensorProto.FLOAT, ["x", "y"])
    node_def = helper.make_node(
        "XnorPopcountMatMul", ["x", "W"], ["out"], domain="finn"
    )
    modelproto = helper.make_model(
        helper.make_graph([node_def], "test_model", [x], [out], value_info=[W])
    )
    model = ModelWrapper(modelproto)
    model.set_tensor_datatype("x", DataType.BINARY)
    model.set_tensor_datatype("W", DataType.BINARY)
    W_data = np.asarray([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    model.set_initializer("W", W_data)
    # test shape inference
    model = model.transform(InferShapes())
    assert model.get_tensor_shape("out") == [M, N]
    # test datatype inference
    assert model.get_tensor_datatype("out") is DataType.FLOAT32
    model = model.transform(InferDataTypes())
    assert model.get_tensor_datatype("out") is DataType.UINT32
    # test execution
    x_data = np.asarray([[1, 0, 0]], dtype=np.float32)
    inp_dict = {"x": x_data}
    out_dict = oxe.execute_onnx(model, inp_dict)
    Wb = 2 * W_data - 1
    xb = 2 * x_data - 1
    rb = np.matmul(xb, Wb)
    assert (2 * out_dict["out"] - K == rb).all()


def test_convert_bipolar_matmul_to_xnorpopcountmatmul():
    lfc = get_test_model_trained("LFC", 1, 1)
    bo.export_finn_onnx(lfc, (1, 1, 28, 28), export_onnx_path)
    model = ModelWrapper(export_onnx_path)
    model = model.transform(InferShapes())
    model = model.transform(FoldConstants())
    model = model.transform(GiveUniqueNodeNames())
    model = model.transform(GiveReadableTensorNames())
    model = model.transform(ConvertSignToThres())
    # load one of the test vectors
    raw_i = get_data("finn", "data/onnx/mnist-conv/test_data_set_0/input_0.pb")
    input_tensor = onnx.load_tensor_from_string(raw_i)
    # run using FINN-based execution
    input_dict = {"global_in": nph.to_array(input_tensor)}
    expected_ctx = oxe.execute_onnx(model, input_dict, True)
    expected = expected_ctx[model.graph.output[0].name]
    model = model.transform(ConvertBipolarMatMulToXnorPopcount())
    produced_ctx = oxe.execute_onnx(model, input_dict, True)
    produced = produced_ctx[model.graph.output[0].name]
    assert np.isclose(expected, produced, atol=1e-3).all()
    os.remove(export_onnx_path)
