classdef test_frames_benchmark < matlab.unittest.TestCase

  properties (TestParameter)
    detector = {@features.det.vlsift};
    dataset = {dset.vgg};
    taskid = {11};
    maxOverlapError = {0.5};
  end
  
  methods (Test)
    function repeatability(test, detector, dataset, taskid, maxOverlapError)
      [~,ima_id] = ismember(dataset.tasks(taskid).ima, {dataset.images.name});
      [~,imb_id] = ismember(dataset.tasks(taskid).imb, {dataset.images.name});
      
      ima_p = dataset.images(ima_id).path;
      fa = detector(single(utls.imread_grayscale(ima_p)));
      
      imb_p = dataset.images(imb_id).path;
      fb = detector(single(utls.imread_grayscale(imb_p)));
      
      g = dataset.tasks(taskid);
      matchFrames = @(fa, fb) geom.ellipse_overlap_H(g, fa, fb, ...
        'maxOverlapError', maxOverlapError);
      
      res = bench.detrep(matchFrames, fa, fb);
      [rep_vgg, nm_vgg] = legacy.vgg_frames_benchmark(g, ...
        ima_p, fa.frames, [], imb_p, fb.frames, [], ...
        'maxOverlapError', maxOverlapError);
      test.verifyEqual(res.repeatability, rep_vgg, 'AbsTol', 1e-3);
      test.verifyEqual(res.numCorresp, nm_vgg, 'AbsTol', 1);
    end
    
    function matchingscore(test, detector, dataset, taskid, maxOverlapError)
      [~,ima_id] = ismember(dataset.tasks(taskid).ima, {dataset.images.name});
      [~,imb_id] = ismember(dataset.tasks(taskid).imb, {dataset.images.name});
      
      ima_p = dataset.images(ima_id).path;
      fa = detector(single(utls.imread_grayscale(ima_p)));
      
      imb_p = dataset.images(imb_id).path;
      fb = detector(single(utls.imread_grayscale(imb_p)));
      
      g = dataset.tasks(taskid);
      matchFrames = @(fa, fb, varargin) geom.ellipse_overlap_H(g, fa, fb, ...
        'maxOverlapError', maxOverlapError, varargin{:});
      
      res = bench.detmatch(matchFrames, fa, fb);
      [~, ~, ms_vgg, nm_vgg] = ...
        legacy.vgg_frames_benchmark( g, ima_p, fa.frames, single(fa.descs), ...
        imb_p, fb.frames, single(fb.descs), 'maxOverlapError', maxOverlapError);
      test.verifyEqual(res.matchingScore, ms_vgg, 'RelTol', 0.01);
      test.verifyEqual(res.numCorresp, nm_vgg, 'RelTol', 0.01);
    end
    
  end
  
end
