Test Baseline Benchmark (W1BS)
=========================================================
This is how to run the baseline matching benchmark.

.. code-block:: python

    # Define baseline benchmark
    bench = bench.W1BSBench.W1BSBench()
    
    # Define feature
    np_sift_py = features.np_sift.np_sift()

    # Define dataset
    w1bs = dset.W1BS_dataset.W1BS_Dataset()
    
    # Do the evaluation
    result_py = bench.evaluate(w1bs, np_sift_py, use_cache=True, save_result=True)

    # Make the results from different detectors as a list. 
    result_list = [result_py]

    # Show the result
    bench.Utils.print_result(result_list, 'ap')


Full code (test/test_W1BS_Bench.py):

.. literalinclude:: ../test/test_W1BS_Bench.py
