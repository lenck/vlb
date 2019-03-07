About This Project
============================

A framework for local feature evaluation.
Reimplementation of the VLBenchmarks project.

MATLAB implementation: `Karel Lenc <https://github.com/lenck>`_

Python implementation: `Xu Zhang <https://github.com/spongezhang>`_

Python Interface
-------------------------

Requirement
^^^^^^^^^^^^^^^^^^^^^^^^

We recommend to use conda to install all the requirements all at once. 


``conda env create -f ./python/conda/environment.yml``


Test the code
^^^^^^^^^^^^^^^^^^^^^^^^^

Test repeatability benchmark

>>> python ./python/test/test_rep_bench.py


Test matching score benchmark

>>> python ./python/test/test_ms_bench.py


Test image retrieval benchmark

>>> python ./python/test/test_retrieval_bench.py


Test wide baseline matching benchmark

>>> python ./python/test/test_W1BS_Bench.py

Test feature extraction

>>> python ./python/test/test_feature_extraction.py

Test draw feature

>>> python ./python/test/draw_frame.py
