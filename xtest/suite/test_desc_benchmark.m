classdef test_desc_benchmark < matlab.unittest.TestCase

  properties (TestParameter)
    category = {'boat', 'graf', 'wall'};
    imid = {2};
    maxOverlapError = {0.5};
  end
  
  methods (Test)
    function pr(test, category, imid, maxOverlapError)
      imdb = vlb_dataset_vggaffine(category);
      
      ima_p = fullfile(imdb.imageDir, imdb.images.name{1});
      [fa, da] = vl_sift(single(utls.imread_grayscale(ima_p)));
      imb_p = fullfile(imdb.imageDir, imdb.images.name{imid});
      [fb, db] = vl_sift(single(utls.imread_grayscale(imb_p)));
      
      geom = imdb.images.geometry(imid);
      matchFrames = @(fa, fb) vlb_ellipse_overlap_H(geom, fa, fb, ...
        'maxOverlapError', maxOverlapError, 'mode', 'descriptors');
      methods =  {'threshold', 'nn', 'nndistratio'};
      results = struct();
      results_vgg = legacy.vgg_desc_benchmark( geom, ima_p, fa, da, ...
        imb_p, fb, db, 'maxOverlapError', maxOverlapError);
      for mi = 1:numel(methods)
        [results.(methods{mi}).precision, results.(methods{mi}).recall] =  ...
          vlb_desc_benchmark(matchFrames, fa, da, fb, db, ...
          'matchingStrategy', methods{mi});
      end
      if 1
        figure(1); clf;
        colors = lines(numel(methods));
        for mi = 1:numel(methods)
          plot(results.(methods{mi}).recall, results.(methods{mi}).precision, ...
            'Color', colors(mi, :)); hold on;
          plot(results_vgg.(methods{mi}).recall, results_vgg.(methods{mi}).precision, ...
            'Color', colors(mi, :), 'LineStyle', '--'); hold on;
        end
        drawnow; 
      end
      
      for mi = 1:numel(methods)
        res = [results.(methods{mi}).recall; results.(methods{mi}).precision];
        res_vgg = [results_vgg.(methods{mi}).recall; results_vgg.(methods{mi}).precision];
        d = test.find_closest(res, res_vgg);
        test.verifyTrue(all(d < 1e-4));
      end
    end
    
  end
  
  methods (Static)
    function dist = find_closest(da, db)
      dist = zeros(1, size(db, 2));
      for dd = 1:size(db, 2)
        dist(dd) = min(sum(bsxfun(@minus, da, db(:, dd)).^2, 1));
      end
    end
  end
  
end
