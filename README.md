## Description

This is a fork of the <a href="https://github.com/Xilinx/finn" target="_blank">official FINN repository</a>, based on commit ```d0ecac226902ed03a35de587bcf72f8f4bfb65fc```.

It is customized for running Backbone and Detection Head parts of PointPillars network (see <a href="https://arxiv.org/abs/1812.05784" target="_blank">paper</a>).
It is meant to run on <a href="https://www.xilinx.com/products/boards-and-kits/zcu104.html" target="_blank">ZCU104</a> board.


## Getting started

Steps for running the PointPillars network through FINN:
1. Clone this repo: ```git clone -b pointpillars https://gitlab.com/konrad966/finn_fork.git```

2. Go to the cloned repo directory.

3. Clone forked PointPillars repo: ```git clone -b working_on_finn https://gitlab.com/konrad966/pointpillars_quantized.git ./pointpillars``` - it may be necessary to run through its README for getting everything going.

4. Clone PYNQ-HelloWorld: ```git clone https://github.com/maltanar/PYNQ-HelloWorld.git```

5. If you use Vivado version other than 2019.1, change line ```set scripts_vivado_version 2019.1``` in file ```PYNQ-HelloWorld/boards/ZCU104/resizer/bitstream/resizer.tcl``` to the appropiate Vivado version.
The FINN workflow for PointPillars was tested on 2019.2

6. Go through README of original FINN repository (commit ```d0ecac226902ed03a35de587bcf72f8f4bfb65fc```)

7. Run notebook ```end2end_example/pointpillars_finn.ipynb``` - it was adapted from ```cnv_end2end_example.ipynb``` notebook.


## Changing network parameters

You may want to run your own version of PointPillars through FINN.
Then, you need to train such a model and save state dict of RPN part into file ```pp_net_params/rpn_weights```.
The RPN class definition in ```pointpillars_finn.ipynb``` may need to be changed, respectively to your version of PointPillars.