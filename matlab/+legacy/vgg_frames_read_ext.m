function [out] = vgg_frames_read_ext(framesFile)
% VGG_FRAMES_READ Read file exported by some of the older frame detectors.
%   FRAMES = VGG_FRAMES_READ(FRAME_FILE_PATH) Reads FRAMES from a file
%   defined by FRAME_FILE_PATH
%
%   vl_ubscread cannot be used because some older detectors produce files
%   which contain length of the descriptors = 1 which the vl_ubcread function
%   is not able to handle.

% Copyright (C) 2011-16 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

fid = fopen(framesFile, 'r');
if fid==-1, error('Could not read file: %s\n', framesFile); end
[header, count] = fscanf(fid, '%f', 2);
if count ~= 2
  fclose(fid);
  error('Invalid frames format.');
end
numPoints = header(2);
[data, count] = fscanf(fid,'%f', [12, numPoints]);
fclose(fid);
if count ~= 12 * numPoints, error('Invalid frames format.'); end
% Transform the frame properly
% X Y CORNERNESS SCALE/3 ANGLE TYPE LAP EXTR M11 M12 M21 M22
frames = zeros(6, numPoints);
frames(1:2,:) = data(1:2,:) + 1;
frames(3:6,:) =  bsxfun(@times, data(9:12, :), data(4, :)) .* 3;
out.frames = utls.frame2ellipse(frames);

out.detresponses = data(3, :);
out.type = data(6, :);
end