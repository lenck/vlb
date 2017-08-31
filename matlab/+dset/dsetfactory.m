function [ imdb ] = dsetfactory( imdbname, varargin )
%VLB_DSET Dataset Factory

if isstruct(imdbname), imdb = imdbname; return; end;
switch imdbname
  case 'vggh'
    imdb = dset.vggh(varargin{:});
  case 'hannoverh'
    imdb = dset.hannoverh(varargin{:});
  case 'hsequences'
    imdb = dset.hsequences(varargin{:});
  otherwise
    error('Unknown dataset %s', imdbname);
end

end

