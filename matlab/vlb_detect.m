function dest_feats_name = vlb_detect(imdb, detector, varargin)
import features.*;

opts.override = false;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detector = features.factory('det', detector, varargin{:});

impaths = {imdb.images.path};
imnames = {imdb.images.name};
dest_dir = vlb_path('features', imdb, detector);
dest_feats_name = detector.name;
vl_xmkdir(dest_dir);

fprintf('Computing detections %s for %d images.\n', ...
  detector.name, numel(impaths));
fprintf('Resulting features are going to be stored in:\n%s.\n', dest_dir);
status = utls.textprogressbar(numel(impaths), 'startmsg', ...
  sprintf('Computing %s ', detector.name), 'updatestep', 1);
for si = 1:numel(impaths)
  impath = impaths{si};
  imname = imnames{si};
  feats_path = fullfile(dest_dir, imname);
  feats = utls.features_load(feats_path, 'checkonly', true);
  if ~isempty(feats) && ~opts.override
    status(si); continue;
  end
  im = imread(impath);
  feats = detector.fun(im);
  utls.features_save(feats_path, feats);
  status(si);
end
end
