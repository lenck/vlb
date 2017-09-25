classdef test_detrepthr_benchmark < matlab.unittest.TestCase

  properties (TestParameter)
    detector = {@features.det.vlcovdet};
    dataset = {dset.vggh};
    taskid = {1, 6, 11};
  end
  
  methods (Test)
    function repeatability(test, detector, dataset, taskid)
      [~,ima_id] = ismember(dataset.tasks(taskid).ima, {dataset.images.name});
      [~,imb_id] = ismember(dataset.tasks(taskid).imb, {dataset.images.name});
      
      ima_p = dataset.images(ima_id).path;
      fa = detector(single(utls.imread_grayscale(ima_p)));
      
      imb_p = dataset.images(imb_id).path;
      fb = detector(single(utls.imread_grayscale(imb_p)));
      
      g = dataset.tasks(taskid);
      matchFrames = @(fa, fb) geom.ellipse_overlap_H(g, fa, fb, ...
        'maxOverlapError', 0.5);
      
      res = bench.detrepthr(matchFrames, fa, fb);
      test.verifyLessThanOrEqual(res.repeatability, 1);
      if 1
        figure(1);
        subplot(1,2,1); hold on;
        plot(res.numDets, res.repeatability);
        drawnow;
        subplot(1,2,2); hold on;
        plot(res.numMatches, res.repeatability);
        drawnow;
      end
    end
  end
  
end
