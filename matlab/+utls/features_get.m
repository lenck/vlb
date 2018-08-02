function [feats, featpath] = features_get(imdb, featsname, imname, varargin)

featsdir = vlb_path('features', imdb, struct('name', featsname));
if ~isdir(featsdir)
    utls.features_not_found(featsdir);
end
featpath = fullfile(featsdir, imname);
feats = utls.features_load(featpath, varargin{:});
if isempty(feats)
  error('Unalbe to find %s features for image %s.', featsname, imname);
end
end