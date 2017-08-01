function [ out, varargin ] = vlb_desc( descname, varargin )
% VLB_DESC Descriptor Factory
opts.descName = descname;
opts.descArgs = {};
[opts, varargin] = vl_argparse(opts, varargin);

if isstruct(descname), out = descname; return; end;

fname = ['desc.' strtrim(descname)];
desc_fun = str2func(fname);
out = struct('fun', @(p) desc_fun(p, opts.descArgs{:}), ...
  'args', {opts.descArgs}, 'name', opts.descName);

end
