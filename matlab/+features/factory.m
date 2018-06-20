function [ res, varargin ] = factory( type, name, varargin )

%   feature name preference:
%      - 'detName' argumnt
%      - function's second output
%      - function name
assert(ismember(type, {'det', 'desc', 'detdesc'}));
opts.([type, 'Name']) = '';
opts.([type, 'Args']) = {};
opts.rootpackage = 'features';
[opts, varargin] = vl_argparse(opts, varargin);
funargs = opts.([type, 'Args']);

if isstruct(name)
  res = name;
  res.type = type;
  assert(isfield(res, 'name') && isfield(res, 'fun'), ...
    'Invalid algorithm structure, must contain `name` and `fun`.');
  return;
end
switch class(name)
  case 'char'
    fname = [opts.rootpackage '.', type, '.' strtrim(name)];
    fun = str2func(fname);
  case 'function_handle'
    fun = name;
  otherwise
    error('Invalid detdesc');
end
try
  nout = nargout(fun);
catch
  error('Invalid %s: %s - Function not found', type, fname);
end
assert(nout >= 1, 'Feature wrapper does not return meta information.');
func_nargin = nargin(fun);
if func_nargin < 0, func_nargin = abs(func_nargin) - 1; end
switch func_nargin
  case 1
    f = fun([], funargs{:});
    res.fun = @(a) fun(a, funargs{:});
  case 2
    f = fun([], [], funargs{:});
    res.fun = @(a, b) fun(a, b, funargs{:});
end
assert(isfield(f, [type, 'Name']), ...
  'Feature wrapper does not return meta information.');
res.name = f.([type, 'Name']);
if ~isempty(opts.([type, 'Name']))
  res.name = opts.([type, 'Name']);
end
if isfield(f, 'describes'), res.describes = f.describes; end;
res.args = opts.([type, 'Args']);
res.type = type;

end
