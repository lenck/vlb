# Feature Detectors and Descriptors:
Most detectors and descriptors utilize opencv for there calculation, however, newer deep
implementation require learned weights to initialize the detection and description networks. These weights are not provided in the repo, but if you wish to test on TODO: INSERT LIST OF DETECTORS, you can use ```download_weights.sh``` to retrieve these weights and extract them to the correct folder.

## Specific Requirements for descriptors

- deepdesc:
    - Need to install torch and LuaJIT on machine
    - To install torch to home directory
    ```
    git clone https://github.com/torch/distro.git ~/torch --recursive
    cd ~/torch; bash install-deps;
    ./install.sh
    ```
    - Then you can install lua modules:
    ```
    luarocks install nn
    ```
    - Finally install lutropy
    ```sudo pip install lutropy
    ```

- hardnet
    - need to install Caffe and Pycaffe
