function [dest_feats_name, feats] = vlb_detect(imdb, detector, varargin)
import features.*;

opts.override = false;
opts.imids = [];
opts.catchErrs = false;
opts.storeFeatures = true;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.factory(imdb);
if isempty(opts.imids), opts.imids = 1:numel(imdb.images); end
detector = features.factory('det', detector, varargin{:});

impaths = {imdb.images(opts.imids).path};
imnames = {imdb.images(opts.imids).name};
dest_dir = vlb_path('features', imdb, detector);
dest_feats_name = detector.name;
vl_xmkdir(dest_dir);

fprintf('Running detector `%s` for %d images of dset `%s`.\n', ...
  detector.name, numel(impaths), imdb.name);
fprintf('Resulting features are going to be stored in:\n%s.\n', dest_dir);
status = utls.textprogressbar(numel(impaths), 'startmsg', ...
  sprintf('Computing %s ', detector.name), 'updatestep', 1);
all_feats = cell(1, numel(impaths));
for si = 1:numel(impaths)
  impath = impaths{si};
  imname = imnames{si};
  feats_path = fullfile(dest_dir, imname);
  feats = utls.features_load(feats_path, 'checkonly', true, ...
    'compulsoryFields', {'frames.csv'});
  if ~isempty(feats) && ~opts.override
    status(si); continue;
  end
  im = imread(impath);
  if opts.catchErrs
    try
      feats = detector.fun(im);  
    catch e
      feats = struct('failed', true, 'impath', impath, 'error', e);
      continue;
    end
  else
    feats = detector.fun(im);
  end
  if opts.storeFeatures
    utls.features_save(feats_path, feats);
  end
  if nargout > 1, all_feats{si} = feats; end
  status(si);
end
end
