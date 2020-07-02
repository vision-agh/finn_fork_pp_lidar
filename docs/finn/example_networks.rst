.. _example_networks:

****************
Example Networks
****************

FINN uses `several pre-trained QNNs <https://github.com/Xilinx/brevitas/tree/master/brevitas_examples/bnn_pynq>`_ that serve as examples and testcases.
You can find a status summary below for each network.

* TFC, SFC, LFC... are fully-connected networks trained on the MNIST dataset
* CNV is a convolutional network trained on the CIFAR-10 dataset
* w\_a\_ refers to the quantization used for the weights (w) and activations (a) in bits

The rows in the table are different steps of the FINN end-to-end flow.
If a particular network is supported for a particular step in the current FINN
version, this is indicated by an x mark in the table.

+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| FINN step             | Basic test | TFC-w1a1 | TFC-w1a2 | TFC-w2a2 | CNV-w1a1 | CNV-w1a2 | CNV-w2a2 |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| Export/Import         | x          | x        | x        | x        | x        |    x     |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| Streamlining          | x          | x        | x        | x        | x        |          |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| Convert to HLS layers | x          | x        | x        | x        | x        |          |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| Stitched IP           | x          | x        | x        | x        | x        |          |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| Hardware test         | x          | x        | x        |          | x        |          |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| cppsim                | x          | x        | x        | x        | x        |          |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| rtlsim node-by-node   | x          | x        | x        | x        | x        |          |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
| rtlsim stitched IP    | x          | x        | x        | x        | x        |          |     x    |
+-----------------------+------------+----------+----------+----------+----------+----------+----------+
