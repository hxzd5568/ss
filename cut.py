import onnx
from onnx import helper, shape_inference
from onnx import TensorProto
import numpy as np
shape = [3, 3]
X = helper.make_tensor_value_info('X', TensorProto.FLOAT, shape)
Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, shape)


add = helper.make_node(
    'Add',
    ['X', 'Y'],
    ['Z']
)
sqrt = helper.make_node(
    'Sqrt',                  # name
    ['Z',], # inputs
    ['out'],                  # outputs
)

out = helper.make_tensor_value_info('out', TensorProto.FLOAT, [3,3])
graph_def = helper.make_graph(
    [add, sqrt, 
    ],        # nodes
    'test-model',      # name
    [X, Y],  # inputs
    [out],  # outputs
)

model_def = helper.make_model(graph_def, producer_name='onnx-example')

#print('The model is:\n{}'.format(model_def))
onnx.checker.check_model(model_def)
#print('The model is checked!')

inferred_model = shape_inference.infer_shapes(model_def)

onnx.save(inferred_model, 'simple.onnx')
onnx.checker.check_model(inferred_model)
print('After shape inference, the shape info of Y is:\n{}'.format(inferred_model.graph.value_info))
