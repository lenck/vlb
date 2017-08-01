function [ frames, name ] = vlcovdet( img, varargin )

opts.Method = 'Dog';
[opts, varargin] = vl_argparse(opts, varargin);
name = sprintf('vlcovdet-%s', opts.Method);
if isempty(img), frames = []; return; end;

frames = vl_covdet(img, 'Method', opts.Method, varargin{:});

end

