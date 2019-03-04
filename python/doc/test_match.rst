Test Feature and Descripor Matching Benchmark
=========================================================
This is how to run the feature matching (repeatability) and descriptor matching (matching score) benchmark.

Repeatablity Benchmark:

.. code-block:: python

    # Define retrieval benchmark
    rep_bench = bench.repBench.repBench()
    
    # Define feature 
    vlsift_py = features.cyvlsift_official.cyvlsift_official()

    # Define dataset
    vggh = dset.vgg_dataset.vggh_Dataset()

    # Do the evaluation
    rep_result_py = rep_bench.evaluate(
        vggh, vlsift_py, use_cache=False, save_result=True)

    # Make the results from different detectors as a list. 
    # (Only one here, but you can add more)
    rep_result = [rep_result_py]

    # Show the result
    for result_term in rep_result[0]['result_term_list']:
        bench.Utils.print_result(rep_result, result_term)
        bench.Utils.save_result(rep_result, result_term)

    #Show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in rep_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(rep_result, sequence, result_term)
            bench.Utils.save_sequence_result(rep_result, sequence, result_term)


Matching score Benchmark:

.. code-block:: python

    # Define matching score benchmark
    ms_bench = bench.MatchingScoreBench.MatchingScoreBench()

    # Define feature 1
    vlsift_py = features.cyvlsift_official.cyvlsift_official()

    # Define feature 2
    vlsift_load_matlab = features.vlsift_load_matlab.vlsift_load_matlab()
    
    # Define dataset
    vggh = dset.vgg_dataset.vggh_Dataset()

    # Do the evaluation
    ms_result_py = ms_bench.evaluate(
        vggh, vlsift_py, use_cache=True, save_result=True)

    ms_result_matlab = ms_bench.evaluate(
        vggh, vlsift_load_matlab, use_cache=True, save_result=True)
    
    # Make the results from different detectors as a list. 
    ms_result = [ms_result_py, ms_result_matlab]

    # Show the result
    for result_term in ms_result[0]['result_term_list']:
        bench.Utils.print_result(ms_result, result_term)
        bench.Utils.save_result(ms_result, result_term)

    #show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in ms_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(ms_result, sequence, result_term)
            bench.Utils.save_sequence_result(ms_result, sequence, result_term)


Full code for Repeatablity Benchmark (test/test_retrieval_bench.py):

.. literalinclude:: ../test/test_rep_bench.py

Full code for Matching Score Benchmark (test/test_ms_bench.py):

.. literalinclude:: ../test/test_ms_bench.py
