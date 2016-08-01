classdef test_frames_get_orientation < matlab.unittest.TestCase
  methods (Test)
    function getimage(test)
      or = linspace(-pi, pi, 36);
      or_r = zeros(1, numel(or));
      for oi = 1:numel(or)
        fra = [0, 0, 10, or(oi)]';
        fra_a = vl_frame2oell(fra);
        or_r(oi) = utls.frame_get_orientation(fra_a);
      end
      test.verifyLessThan(max(or_r - or), 1e-10);
    end
  end
end
