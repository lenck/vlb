function [ frames, info ] = vlcovdet( img, varargin )

opts.Method = 'Dog';
[opts, varargin] = vl_argparse(opts, varargin);
info.name = sprintf('vlcovdet-det-%s', opts.Method);
if isempty(img), frames = zeros(6, 0); return; end;
img = utls.covdet_preprocessim(img);

frames = vl_covdet(img, 'Method', opts.Method, varargin{:});

end

