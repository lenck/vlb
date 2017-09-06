function [ res ] = matdet( img, varargin )
%MATDET Summary of this function goes here
%   Detailed explanation goes here
opts.detector = 'fast';
[opts, varargin] = vl_argparse(opts, varargin);

dets = struct();
dets.fast = @detectFASTFeatures;
dets.surf = @detectSURFFeatures;
dets.brisk = @detectBRISKFeatures;
dets.mser = @detectMSERFeatures;

if ~isfield(dets, opts.detector)
  error('Invalid detector. Valid options are: %s', strjoin(fieldnames(dets)));
end
fun = dets.(opts.detector);
res.detName = sprintf('matdet-%s', opts.detector);
if isempty(img), res.frames = zeros(6, 0); return; end;
if size(img, 3) > 1, img = rgb2gray(img); end;

fp = fun(img, varargin{:});

res.frames = double(fp.Location');
if isprop(fp, 'Scale'), res.frames = [res.frames; fp.Scale']; end
if isprop(fp, 'Orientation'), res.frames = [res.frames; fp.Orientation']; end
if isprop(fp, 'Metric'), res.peakScores = fp.Metric'; end
if isprop(fp, 'Axes') % MSER
  res.frames = [double(fp.Location'); zeros(4, numel(fp.Orientation))];
  for fi = 1:numel(fp.Orientation)
    aff = [fp.Axes(fi, 1)./2, 0; 0, fp.Axes(fi, 2)./2];
    ang = fp.Orientation(fi);
    aff = [cos(ang), sin(ang); -sin(ang), cos(ang)] * aff;
    res.frames(3:6, fi) = utls.afftf2frame(aff);
  end
  
  if 0 % Debug code
    clf;
    imshow(img); hold on;
    plot(fp);
    vl_plotframe(res.frames, 'LineWidth', 1, 'Color', 'k');
  end
end

end
