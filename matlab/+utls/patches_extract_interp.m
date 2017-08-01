function [ patches, varargin ] = extract_patches_interp( ima, fms, varargin )
%EXTRACT_PATCHES_COVDET Extract patches using VL_COVDET
opts.patchResolution = 32;
opts.PatchRelativeExtent = 3*sqrt(3);
opts.method = 'linear';
if nargout == 1
  opts = vl_argparse(opts, varargin);
else
  [opts, varargin] = vl_argparse(opts, varargin);
end
args = helpers.struct2args(opts);

is_uint = isa(ima, 'uint8');
if is_uint, ima = single(ima) ./ 255; end
if size(ima, 3) == 3, ima = rgb2gray(ima); end;

outsz = opts.patchResolution*2 + 1;
patches = zeros(outsz, outsz, 1, size(fms, 2), 'like', ima);
s = linspace(-1, 1, outsz);
[R_n, C_n] = ndgrid(s, s);
P_n = [C_n(:), R_n(:)]';

for pi = 1:size(fms, 2)
  H = utls.frame2afftf(utls.frame_magnify_scale(fms(:, pi), opts.PatchRelativeExtent));
  P_i = helpers.p2e(H*helpers.e2p(P_n)) + 1;
  % 'Query' rows and columns
  R_i = reshape(P_i(2,:), outsz, outsz);
  C_i = reshape(P_i(1,:), outsz, outsz);
  patches(:,:,pi) = interp2(ima, C_i, R_i, opts.method);
end

if is_uint, patches = uint8(patches * 255); end

end

