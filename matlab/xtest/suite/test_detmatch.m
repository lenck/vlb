classdef test_detmatch < matlab.unittest.TestCase

  properties (TestParameter)
    detector = {@features.det.vlsift};
    dataset = {dset.vggh};
    taskid = {1, 6, 11};
  end
  
  methods (Test)    
    function kmequal(test, detector, dataset, taskid)
      task = dataset.tasks(taskid);
      ima_p = dataset.images(task.ima_id).path;
      fa = detector(single(utls.imread_grayscale(ima_p)));    
      imb_p = dataset.images(task.imb_id).path;
      fb = detector(single(utls.imread_grayscale(imb_p)));
      
      matchFrames = @(fa, fb, varargin) geom.ellipse_overlap_H(task, fa, fb, ...
        'maxOverlapError', 0.4, varargin{:});
      
      res = bench.detmatch(matchFrames, fa, fb);
      [~, ~, ms_vgg, nm_vgg] = ...
        legacy.vgg_frames_benchmark( task, ima_p, fa, ...
        imb_p, fb, 'maxOverlapError', 0.4);
      test.verifyEqual(res.matchingScore, ms_vgg, 'RelTol', 0.01);
      test.verifyEqual(res.numMatches, nm_vgg, 'RelTol', 0.01);
    end
    
    function emptyoutput(test)
      imdb = dset.vggh();
      task = imdb.tasks(1);
      fa = features.det.vlsift(rand(task.ima_size));
      fb = features.det.vlsift(rand(task.imb_size));
      matchFrames = @(fa, fb, varargin) geom.ellipse_overlap_H(task, fa, fb, ...
        'maxOverlapError', 0.4, varargin{:});
      [res, info] = bench.detmatch(matchFrames, fa, fb);
      fa.frames = []; fa.descs = []; fb.frames = []; fb.descs = [];
      [res_e, info_e] = bench.detmatch(matchFrames, fa, fb);
      test.verifyEqual(fieldnames(res), fieldnames(res_e));
      test.verifyEqual(fieldnames(info), fieldnames(info_e));
    end
  end
  
end
