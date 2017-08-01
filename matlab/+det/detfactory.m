function [ out, varargin ] = detfactory( detname, varargin )
% VLB_DESC Descriptor Factory
%   det name preference:
%      - 'detName' argumnt
%      - function's second output
%      - function name
opts.detName = '';
opts.detArgs = {};
[opts, varargin] = vl_argparse(opts, varargin);

if isstruct(detname), out = detname; return; end;

switch class(detname)
  case 'char'
    fname = ['det.' strtrim(detname)];
    det_fun = str2func(fname);
  case 'function_handle'
    det_fun = detname;
    detname = func2str(detname);
    detname = strrep(detname, 'det.', '');
  otherwise
    error('Invalid detector');
end
if nargout(det_fun) > 1
  [~,detname] = det_fun([], opts.detArgs{:});
end
if ~isempty(opts.detName), detname = opts.detName; end;

out = struct('fun', @(p) det_fun(p, opts.detArgs{:}), ...
  'args', {opts.detArgs}, 'name', detname);

end
