classdef test_descs < matlab.unittest.TestCase
  properties (TestParameter)
    descriptor = utls.listfiles(fullfile(vlb_path(), 'matlab', '+features', '+desc', '*.m'), 'keepext', false, 'fullpath', false);
    image = {rand(0, 0, 1), rand(50, 50, 1),  rand(50, 50, 3), rand(50, 50, 3, 'single'), vl_impattern('roofs1'), im2uint8(vl_impattern('roofs2'))};
    frameType = {'disc', 'oriented_disc'};
  end
  
  methods (Test)
    function testdesc(test, descriptor, image, frameType)
      desc_info = features.factory('desc', descriptor);
      desc_fun = desc_info.fun;
      test.verifyTrue(isfield(desc_info, 'name') == 1);
      test.verifyTrue(isfield(desc_info, 'describes') == 1);
      test.verifyTrue(ismember(desc_info.describes, {'patches', 'frames'}));
      imsize = size(image);
      infeats = features.det.random(image, 'frameType', frameType);
      switch desc_info.describes
        case 'frames'
          feats = desc_fun(image, infeats);
          % Test if the returned frames are valid
          test.verifyTrue(isfield(feats, 'frames') == 1);
          test.verifyTrue(isfield(feats, 'descs') == 1);
          test.verifyEqual(size(feats.descs, 2), size(feats.frames, 2));
          frames = feats.frames;
          if ~isempty(frames)
            test.verifyGreaterThan(frames(1:2,:), 0);
            % Frames in IMAGE coordinates, not Matlab matrix coords
            test.verifyLessThan(frames(2,:), imsize(1)+1);
            test.verifyLessThan(frames(1,:), imsize(2)+1);
          end
        case 'patches'
          patches = utls.patches_extract_covdet(image, infeats.frames);
          feats = desc_fun(patches);
      end
      test.verifyTrue(isfield(feats, 'descs') == 1);
      test.verifyGreaterThanOrEqual(size(feats.descs, 1), 0);
    end
  end
end
