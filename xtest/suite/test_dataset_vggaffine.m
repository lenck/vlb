classdef test_dataset_vggaffine < matlab.unittest.TestCase

  properties (TestParameter)
    category = {'graf'};
  end
  
  methods (Test)
    function getimage(test, category)
      imdb = vlb_dataset_vggaffine(category);
      impath = fullfile(imdb.imageDir, imdb.images.name{1});
      test.verifyEqual(exist(impath, 'file'), 2);
      test.verifyNotEmpty(imread(impath));
    end
  end
  
end
