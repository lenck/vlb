%% PART 1: Image feature detectors
% VLB provides simple wrappers and helper functions for a range of public
% benchmakrs are public datasets. In this example we show some local
% feature detector benchmarks. At first we setup the environemnt:

vlb_setup();

%%
% Next we generate an example image and run some feature detectors on it.
% VLB by default works with frames in the VLFeat format. For details, see
% the documentation of |vl_plotframe|.
blobs = 1 - utls.generate_ellblobs();
siftFrames = vl_sift(single(blobs), 'PeakThresh', 0.1);

imshow(blobs); hold on;
vl_plotframe(siftFrames, 'LineWidth', 2, 'Color', lines(1));
%%
% Similarly, VLB provides 


%%

% --------------------------------------------------------------------
% PART 2: Detector repeatability
% --------------------------------------------------------------------

% A detector repeatability is measured against a benchmark. In this
% case we create an instance of the VGG Affine Testbed (graffity
% sequence).

dataset = datasets.VggAffineDataset('Category','graf');

% Next, the benchmark is intialised by choosing various
% parameters and geometric consistency model. The
% HomographyConsistencyModel corresponds to IJCV04 model where the ground
% truth is defined by homography between pair of images.

repBenchmark = RepeatabilityBenchmark(HomographyConsistencyModel(), ...
  'Mode','Repeatability');

% Prepare three detectors, the two from PART 1 and a third one that
% detects MSER image features.

mser = VlFeatMser();
featExtractors = {siftDetector, thrSiftDetector, mser};

% Now we are ready to run the repeatability test. We do this by fixing
% a reference image A and looping through other images B in the
% set. To this end we use the following information:
%
% dataset.NumImages:
%    Number of images in the dataset.
%
% dataset.getImagePath(i):
%    Path to the i-th image.
%
% dataset.getTransformation(i):
%    Transformation from the first (reference) image to image i.
%
% Like for the detector output (see PART 1), VLBenchmarks caches the
% output of the test. This can be disabled by calling
% repBenchmark.disableCaching().

repeatability = [];
numCorresp = [];

imageAPath = dataset.getImagePath(1);
for d = 1:numel(featExtractors)
  for i = 2:dataset.NumImages
    [repeatability(d,i) numCorresp(d,i)] = ...
      repBenchmark.testFeatureExtractor(featExtractors{d}, ...
                                dataset.getSceneGeometry(i), ...
                                dataset.getImagePath(1), ...
                                dataset.getImagePath(i));
  end
end

% The scores can now be prented, as well as visualized in a
% graph. This uses two simple functions defined below in this file.

detectorNames = {'SIFT','SIFT PT=10','MSER'};
printScores(detectorNames, 100 * repeatability, 'Repeatability');
printScores(detectorNames, numCorresp, 'Number of correspondences');

figure(2); clf; 
plotScores(detectorNames, dataset, 100 * repeatability, 'Repeatability');
helpers.printFigure(resultsPath,'repeatability',0.6);

figure(3); clf; 
plotScores(detectorNames, dataset, numCorresp, 'Number of correspondences');
helpers.printFigure(resultsPath,'numCorresp',0.6);

% Optionally, we can also see the matched frames itself. In this
% example we examine the matches between the reference and fourth
% image.
%
% We do this by running the repeatabiltiy score again. However, since
% the results are cached, this is fast.

imageBIdx = 3;

[drop drop siftSubsRes] = ...
  repBenchmark.testFeatureExtractor(siftDetector, ...
                            dataset.getSceneGeometry(imageBIdx), ...
                            dataset.getImagePath(1), ...
                            dataset.getImagePath(imageBIdx));

% And plot the feature frame correspondences

figure(4); clf;
imshow(dataset.getImagePath(imageBIdx));
benchmarks.helpers.plotFrameMatches(siftSubsRes,...
                                    'IsReferenceImage',false,...
                                    'PlotMatchLine',false,...
                                    'PlotUnmatched',false);
helpers.printFigure(resultsPath,'correspondences',0.75);

% --------------------------------------------------------------------
% PART 3: Detector matching score
% --------------------------------------------------------------------

% The matching score is similar to the repeatability score, but
% involves computing a descriptor. Detectors like SIFT bundle a
% descriptor as well. However, most of them (e.g. MSER) do not have an
% associated descriptor (e.g. MSER). In this case we can bind one of
% our choice by using the DescriptorAdapter class.
%
% In this particular example, the object encapsulating the SIFT
% detector is used as descriptor form MSER.

mserWithSift = DescriptorAdapter(mser, siftDetector);
featExtractors = {siftDetector, thrSiftDetector, mserWithSift};

% We create a benchmark object and run the tests as before, but in
% this case we request that descriptor-based matched should be tested.

matchingBenchmark = RepeatabilityBenchmark(HomographyConsistencyModel(), ...
  'Mode','MatchingScore');

matchScore = [];
numMatches = [];

for d = 1:numel(featExtractors)
  for i = 2:dataset.NumImages
    [matchScore(d,i) numMatches(d,i)] = ...
      matchingBenchmark.testFeatureExtractor(featExtractors{d}, ...
                                dataset.getSceneGeometry(i), ...
                                dataset.getImagePath(1), ...
                                dataset.getImagePath(i));
  end
end

% Print and plot the results

detectorNames = {'SIFT','SIFT PT=10','MSER with SIFT'};

printScores(detectorNames, matchScore*100, 'Match Score');
printScores(detectorNames, numMatches, 'Number of matches') ;

figure(5); clf; 
plotScores(detectorNames, dataset, matchScore*100,'Matching Score');
helpers.printFigure(resultsPath,'matchingScore',0.6);

figure(6); clf; 
plotScores(detectorNames, dataset, numMatches,'Number of matches');
helpers.printFigure(resultsPath,'numMatches',0.6);

% Same as with the correspondences, we can plot the matches based on
% feature frame descriptors. The code is nearly identical.

imageBIdx = 3;
[r nc siftSubsRes] = ...
  matchingBenchmark.testFeatureExtractor(siftDetector, ...
                            dataset.getSceneGeometry(imageBIdx), ...
                            dataset.getImagePath(1), ...
                            dataset.getImagePath(imageBIdx));

figure(7); clf;
imshow(imread(dataset.getImagePath(imageBIdx)));
benchmarks.helpers.plotFrameMatches(siftSubsRes,...
                                    'IsReferenceImage',false,...
                                    'PlotMatchLine',false,...
                                    'PlotUnmatched',false);
helpers.printFigure(resultsPath,'matches',0.75);