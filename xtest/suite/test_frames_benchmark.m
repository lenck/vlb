classdef test_frames_benchmark < matlab.unittest.TestCase

  properties (TestParameter)
    category = {'boat'};
    imid = {2};
    maxOverlapError = {0.5};
  end
  
  methods (Test)
    function repeatability(test, category, imid, maxOverlapError)
      imdb = vlb_dataset_vggaffine(category);
      
      ima_p = fullfile(imdb.imageDir, imdb.images.name{1});
      fa = vl_sift(single(utls.imread_grayscale(ima_p)));
      
      imb_p = fullfile(imdb.imageDir, imdb.images.name{imid});
      fb = vl_sift(single(utls.imread_grayscale(imb_p)));
      
      geom = imdb.images.geometry(imid);
      matchFrames = @(fa, fb) vlb_ellipse_overlap_H(geom, fa, fb, ...
        'maxOverlapError', maxOverlapError);
      
      [rep, nm] = vlb_repeatability(matchFrames, fa, fb);
      [rep_vgg, nm_vgg ] = legacy.vgg_frames_benchmark( geom, ...
        ima_p, fa, [], imb_p, fb, [], 'maxOverlapError', maxOverlapError);
      test.verifyEqual(rep, rep_vgg, 'AbsTol', 1e-3);
      test.verifyEqual(nm, nm_vgg);
    end
    
    function matchingscore(test, category, imid, maxOverlapError)
      imdb = vlb_dataset_vggaffine(category);
      
      ima_p = fullfile(imdb.imageDir, imdb.images.name{1});
      [fa, da] = vl_sift(single(utls.imread_grayscale(ima_p)));
      
      imb_p = fullfile(imdb.imageDir, imdb.images.name{imid});
      [fb, db] = vl_sift(single(utls.imread_grayscale(imb_p)));
      
      geom = imdb.images.geometry(imid);
      matchFrames = @(fa, fb) vlb_ellipse_overlap_H(geom, fa, fb, ...
        'maxOverlapError', maxOverlapError);
      
      [ms, nm] = vlb_matchingscore(matchFrames, fa, da, fb, db);
      [~, ~, ms_vgg, nm_vgg] = ...
        legacy.vgg_frames_benchmark( geom, ima_p, fa, da, imb_p, fb, db, ...
        'maxOverlapError', maxOverlapError);
      test.verifyEqual(ms, ms_vgg, 'RelTol', 0.01);
      test.verifyEqual(nm, nm_vgg, 'RelTol', 0.01);
    end
    
  end
  
end
