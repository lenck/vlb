function [ feature, varargin ] = factory( type, name, varargin )

%   feature name preference:
%      - 'detName' argumnt
%      - function's second output
%      - function name
assert(ismember(type, {'det', 'desc', 'detdesc'}));
opts.([type, 'Name']) = '';
opts.([type, 'Args']) = {};
[opts, varargin] = vl_argparse(opts, varargin);
funargs = opts.([type, 'Args']);

if isstruct(name)
  feature = name;
  assert(isfield(feature, 'name'), isfield(feature, 'fun'));
  return;
end;
switch class(name)
  case 'char'
    fname = ['features.', type, '.' strtrim(name)];
    fun = str2func(fname);
  case 'function_handle'
    fun = name;
  otherwise
    error('Invalid detdesc');
end
assert(nargout(fun) >= 2, 'Feature wrapper does not return meta information.');
func_nargin = nargin(fun);
func_nargout = nargout(fun);
if func_nargin < 0, func_nargin = abs(func_nargin) - 1; end;
assert(func_nargout > 1 && func_nargout <= 3);
switch func_nargin
  case 1
    switch func_nargout
      case 2
        [~, feature] = fun([], funargs{:});
      case 3
        [~, ~, feature] = fun([], funargs{:});
    end
    feature.fun = @(a) fun(a, funargs{:});
  case 2
    switch func_nargout
      case 2
        [~, feature] = fun([], [], funargs{:});
      case 3
        [~, ~, feature] = fun([], [], funargs{:});
    end
    feature.fun = @(a, b) fun(a, b, funargs{:});
end
if ~isempty(opts.([type, 'Name']))
  feature.name = opts.([type, 'Name']);
end
feature.args = opts.([type, 'Args']);

end
