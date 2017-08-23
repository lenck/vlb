classdef test_dets < matlab.unittest.TestCase
  properties (TestParameter)
    detector = utls.listfiles(fullfile(vlb_path(), 'matlab', '+features', '+det', '*.m'), 'keepext', false, 'fullpath', false);
    image = {rand(0, 0, 1), rand(50, 50, 1),  rand(50, 50, 3), rand(50, 50, 3, 'single'), vl_impattern('roofs1'), im2uint8(vl_impattern('roofs2'))};
  end
  
  methods (Test)
    function testdet(test, detector, image)
      % Try if this works
      det = features.factory('det', detector);
      % Create the functor from scratch
      det_fun = str2func(['features.det.', detector]);
      test.verifyEqual(nargout(det_fun), 1);
      [det_info] = det_fun([]);
      test.verifyTrue(isfield(det_info, 'detName'));
      imsize = size(image);
      feats = det_fun(image);
      test.verifyTrue(isfield(feats, 'frames'));
      frames = feats.frames;
      test.verifyGreaterThanOrEqual(size(frames, 1), 2);
      test.verifyLessThanOrEqual(size(frames, 1), 6);
      if ~isempty(frames)
        test.verifyGreaterThan(frames(1:2,:), 0);
        % Frames in IMAGE coordinates, not Matlab matrix coords
        test.verifyLessThan(frames(2,:), imsize(1)+1);
        test.verifyLessThan(frames(1,:), imsize(2)+1);
      end
    end
  end
end
