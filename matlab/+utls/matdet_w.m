function [ frames, descs, info ] = matdet_w( fp )
descs = [];
info = struct();
frames = double(fp.Location');
if isprop(fp, 'Scale'), frames = [frames; fp.Scale']; end
if isprop(fp, 'Orientation'), frames = [frames; fp.Orientation']; end
if isprop(fp, 'Metric')
  info.peakScores = fp.Metric';
end

end

