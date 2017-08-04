classdef test_detdescs < matlab.unittest.TestCase
  properties (TestParameter)
    detector = utls.listfiles(fullfile(vlb_path(), 'matlab', '+features', '+detdesc', '*.m'), 'keepext', false, 'fullpath', false);
    image = {rand(0, 0, 1), rand(50, 50, 1),  rand(50, 50, 3), rand(50, 50, 3, 'single'), vl_impattern('roofs1'), im2uint8(vl_impattern('roofs2'))};
  end
  
  methods (Test)
    function testdetdesc(test, detector, image)
      % Try if this works
      det = features.factory('detdesc', detector);
      % Create the functor from scratch
      det_fun = str2func(['features.detdesc.', detector]);
      test.verifyEqual(nargout(det_fun), 3);
      [~, ~, det_info] = det_fun([]);
      test.verifyTrue(isfield(det_info, 'name'));
      imsize = size(image);
      [frames, descriptors, ~] = det_fun(image);
      test.verifyGreaterThanOrEqual(size(frames, 1), 2);
      test.verifyLessThanOrEqual(size(frames, 1), 6);
      test.verifyEqual(size(frames, 2), size(descriptors, 2));
      if ~isempty(frames)
        test.verifyGreaterThan(frames(1:2,:), 0);
        % Frames in IMAGE coordinates, not Matlab matrix coords
        test.verifyLessThan(frames(2,:), imsize(1)+1);
        test.verifyLessThan(frames(1,:), imsize(2)+1);
      end
    end
  end
end
