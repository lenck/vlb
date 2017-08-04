function [ frames, info ] = random( img, varargin )
%RANDOM Summary of this function goes here
%   Detailed explanation goes here
opts.featuresDensity = 2e-3;
opts.frameType = 'disc';
opts.maxScale = 30;
opts.minScale = 0.1;
opts = vl_argparse(opts, varargin);
info.name = sprintf('random-%s', opts.frameType);
if isempty(img), frames = zeros(5, 0); return; end;


imgSize = size(img);
img = double(img) ;
q = RandStream('mt19937ar','Seed', mean(img(:)));

imageArea = imgSize(1) * imgSize(2);
numFeatures = round(imageArea * opts.featuresDensity);

locations = rand(q, 2,numFeatures);
locations(1,:) = locations(1,:) .* imgSize(2);
locations(2,:) = locations(2,:) .* imgSize(1);
scales = rand(q, 2, numFeatures)*(opts.maxScale - opts.minScale) + opts.minScale;
angles = rand(1,numFeatures) * 2*pi;

switch opts.frameType
  case 'disc'
    frames = [locations; scales(1,:)];
  case 'oriented_disc'
    frames = [locations; scales(1, :); angles];
  otherwise
    error('Invalid frame type');
end

end

