function [ patches, varargin ] = patches_extract_covdet( ima, fms, varargin )
%EXTRACT_PATCHES_COVDET Extract patches using VL_COVDET
opts.patchResolution = 32;
opts.baseScale = 0.6;
opts.patchRelativeSmoothing = 0.1;
opts.doubleImage = true;
opts.scalingFactor = 1;
[opts, varargin] = vl_argparse(opts, varargin);
args = utls.struct2argscell(opts);
args = args(1:end-2);

if isempty(ima) || isempty(fms),patches = []; return; end;
is_uint = isa(ima, 'uint8');
ima = utls.covdet_preprocessim(ima);

[~, patches] = vl_covdet(ima, 'frames', fms, 'Descriptor', 'patch', ...
  'PatchRelativeExtent', opts.scalingFactor, args{:});
patchesSz = [opts.patchResolution*2 + 1, opts.patchResolution*2 + 1, ...
  1, size(fms,2)];
patches = reshape(patches, patchesSz);

if is_uint, patches = uint8(patches * 255); end

end

