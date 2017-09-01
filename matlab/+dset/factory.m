function [ imdb ] = factory( name, varargin )
%VLB_DSET Dataset Factory

dsets = utls.listfiles(fullfile(vlb_path(), 'matlab', '+dset', '*.m'), ...
  'keepext', false, 'fullpath', false);
dsets = setdiff(dsets, 'factory');
if nargin == 0, imdb = dsets; return; end;
if isstruct(name), imdb = name; return; end;

if ~ismember(name, dsets),
  error('Invalid dataset %s. Valid values are: %s', name, strjoin(dsets, ', '));
end
dsetfun = str2func(['dset.', name]);
imdb = dsetfun(varargin{:});
if ~isfield(imdb, 'name')
  error('Invalid dataset structure %s', name);
end

end

