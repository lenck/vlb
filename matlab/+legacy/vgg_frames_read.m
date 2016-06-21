function frames = vgg_frames_read(framesFile)
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
[frames, count] = fscanf(fid,'%f', [5, numPoints]);
fclose(fid);
if count ~= 5 * numPoints, error('Invalid frames format.'); end
% Transform the frame properly
frames(1:2,:) = frames(1:2,:) + 1;
C = frames(3:5, :);
den = C(1,:) .* C(3,:) - C(2,:) .* C(2,:) ;
S = [C(3,:) ; -C(2,:) ; C(1,:)] ./ den([1 1 1], :) ;
frames(3:5,:) = S;
end