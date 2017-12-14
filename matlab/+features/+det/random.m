function [ res ] = random( img, varargin )
%RANDOM Summary of this function goes here
%   Detailed explanation goes here
opts.featuresDensity = 2e-3;
opts.numFeatures = nan;
opts.frameType = 'disc';
opts.maxScale = 50;
opts.minScale = 0.1;
opts.maxAffScRot = 2*pi;
opts.maxRot = 2*pi;
opts.maxAnisotropy = 2;
opts.anisotropyShift = 0;
opts.seed = mean(double(img(:)));
opts = vl_argparse(opts, varargin);
res.detName = sprintf('random-%s', opts.frameType); res.args = opts;
if isempty(img), res.frames = zeros(5, 0); return; end

stime = tic;
q = RandStream('mt19937ar','Seed', opts.seed);

imgSize = size(img);
imageArea = imgSize(1) * imgSize(2);
if isnan(opts.numFeatures)
  numFeatures = round(imageArea * opts.featuresDensity);
else
  numFeatures = opts.numFeatures;
end
locations = rand(q, 2, numFeatures);
scales = abs(randn(q, 1, numFeatures))*(opts.maxScale - opts.minScale)./3 + opts.minScale;
scales = min(scales, opts.maxScale);

minLoc = [scales; scales]; 
maxLoc = [bsxfun(@plus, -scales, imgSize(2)); bsxfun(@plus, -scales, imgSize(1))];
locations(1,:) = locations(1,:) .* (maxLoc(1,:) - minLoc(1,:)) + minLoc(1, :);
locations(2,:) = locations(2,:) .* (maxLoc(2,:) - minLoc(2,:)) + minLoc(2, :);

res.frames = [locations; scales(1,:)];

switch opts.frameType
  case {'disc', 'oriented_disc'}
    if strcmp(opts.frameType, 'oriented_disc')
      angles = rand(1, numFeatures) * 2*pi;
      res.frames = [res.frames; angles];
    end
  case {'ellipse', 'oriented_ellipse'}
    res.frames = vl_frame2oell(res.frames);
    for fi = 1:numFeatures
      A = utls.randomtf('minScale', 0, 'maxScale', 0, ...
        'maxRot', opts.maxRot, 'maxAnisotropy', opts.maxAnisotropy, ...
        'maxAffScRot', opts.maxAffScRot, 'q', q);
      
      Af = utls.frame2afftf(res.frames(:, fi)) * A;
      res.frames(:, fi) = utls.afftf2frame(Af);
    end
    if ~strcmp(opts.frameType, 'oriented_ellipse')
      res.frames = utls.frame2ellipse(res.frames);
    end
  otherwise
    error('Invalid frame type');
end
res.detresponses = rand(1, numFeatures);
res.dettime = toc(stime);
end

