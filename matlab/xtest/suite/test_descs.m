classdef test_descs < matlab.unittest.TestCase
  properties (TestParameter)
    descriptor = utls.listfiles(fullfile(vlb_path(), 'matlab', '+features', '+desc', '*.m'), 'keepext', false, 'fullpath', false);
    image = {rand(0, 0, 1), rand(50, 50, 1),  rand(50, 50, 3), rand(50, 50, 3, 'single'), vl_impattern('roofs1'), im2uint8(vl_impattern('roofs2'))};
    frameType = {'disc', 'oriented_disc'};
  end
  
  methods (Test)
    function testdet(test, descriptor, image, frameType)
      desc_info = features.factory('desc', descriptor);
      desc_fun = desc_info.fun;
      test.verifyTrue(isfield(desc_info, 'name') == 1);
      test.verifyTrue(isfield(desc_info, 'describes') == 1);
      test.verifyTrue(ismember(desc_info.describes, {'patches', 'frames'}));
      imsize = size(image);
      frames = features.det.random(image, 'frameType', frameType);
      switch desc_info.describes
        case 'frames'
          [frames, descs, ~] = desc_fun(image, frames);
          % Test if the returned frames are valid
          test.verifyGreaterThanOrEqual(size(frames, 1), 2);
          test.verifyLessThanOrEqual(size(frames, 1), 6);
          if ~isempty(frames)
            test.verifyGreaterThan(frames(1:2,:), 0);
            % Frames in IMAGE coordinates, not Matlab matrix coords
            test.verifyLessThan(frames(2,:), imsize(1)+1);
            test.verifyLessThan(frames(1,:), imsize(2)+1);
          end
        case 'patches'
          patches = utls.patches_extract_covdet(image, frames);
          [descs, ~] = desc_fun(patches);
      end
      test.verifyEqual(size(descs, 2), size(frames, 2));
      test.verifyGreaterThanOrEqual(size(descs, 1), 0);
    end
  end
end
