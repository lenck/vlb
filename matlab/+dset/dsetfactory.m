function [ imdb ] = dsetfactory( imdbname, varargin )
%VLB_DSET Dataset Factory

if isstruct(imdbname), imdb = imdbname; return; end;
switch imdbname
  case 'vgg'
    imdb = dset.vgg(varargin{:});
  otherwise
    error('Unknown dataset %s', imdbname);
end

end

