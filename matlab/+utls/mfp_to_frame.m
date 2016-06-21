function [ frames, info ] = mfp_to_frame( fp )

info = struct();
frames = double(fp.Location');
if isprop(fp, 'Scale'), frames = [frames; fp.Scale']; end
if isprop(fp, 'Orientation'), frames = [frames; fp.Orientation']; end
if isprop(fp, 'Metric'), info.peakScores = fp.Metric'; end

end

