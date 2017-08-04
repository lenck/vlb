function [ frames, descriptors, info ] = vlcovdet( img, varargin )

opts.Method = 'Dog';
opts.descriptor = 'sift';
[opts, varargin] = vl_argparse(opts, varargin);
info.name = sprintf('vlcovdet-det-%s-desc-%s', lower(opts.Method), ...
  lower(opts.descriptor));

if isempty(img), frames = zeros(6, 0); descriptors = []; return; end;
img = utls.covdet_preprocessim(img);

[frames, descriptors] = vl_covdet(img, 'Method', opts.Method, varargin{:});

end

