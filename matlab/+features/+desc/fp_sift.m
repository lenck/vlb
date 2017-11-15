function [ res ] = fp_sift( im, feats, varargin )
opts.scalingFactor = 5;
opts.extractPatchesFun = @utls.patches_extract_covdet;
opts.topn = inf;
opts = vl_argparse(opts, varargin);

res = struct('descName', mfilename, 'describes', 'frames', 'descs', [], ...
  'scalingFactor', opts.scalingFactor);
if isempty(im), return; end
feats = utls.topnframes(feats, opts.topn);
res = vl_override(res, feats);
frames = feats.frames;
if isempty(frames), return; end

patches = opts.extractPatchesFun(im, frames, ...
  'scalingFactor', opts.scalingFactor, varargin{:});

res = vl_override(res, features.desc.p_sift(patches));
res.descName = mfilename;
end

