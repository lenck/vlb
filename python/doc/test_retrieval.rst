Test Retrieval Benchmark
======================================================
This is how to run the retrieval benchmark

.. code-block:: python
    
    # Define retrieval benchmark
    retrieval_bench = bench.RetrievalBenchmark.RetrievalBenchmark()

    # Define feature
    vlsift_py = features.cyvlsift_official.cyvlsift_official()
    
    # Define dataset
    paris6k = dset.paris6k_dataset.paris6k_Dataset()

    # Do the evaluation
    map_result_py = retrieval_bench.evaluate(
        paris6k, vlsift_py, use_cache=True, save_result=True)

    # Make the results from different detectors as a list. 
    # (Only one here, but you can add more)
    map_result = [map_result_py]

    # Show the result
    for result_term in map_result[0]['result_term_list']:
        bench.Utils.print_retrieval_result(map_result, 'm' + result_term)
        bench.Utils.save_retrieval_result(map_result, 'm' + result_term)


Full code (test/test_retrieval_bench.py):

.. literalinclude:: ../test/test_retrieval_bench.py
