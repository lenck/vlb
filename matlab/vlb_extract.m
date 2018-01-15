function vlb_extract(imdb, featsname, varargin)

opts.override = false;
opts.grayscale = true;
opts.imgExt = '.png';
opts.scalingFactor = 5;
opts.extractPatchesFun = @utls.patches_extract_covdet;
opts.maxNumFeatures = 10000;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.factory(imdb);
if iscell(featsname), featsname = fullfile(featsname); end;

dets_path = vlb_path('features', imdb, struct('name', featsname));
if ~isdir(dets_path), utls.features_not_found(dets_path); end;
impaths = {imdb.images.path};
imnames = {imdb.images.name};

patches_dir = vlb_path('patches', imdb, struct('name', featsname));
vl_xmkdir(patches_dir);

fprintf('Extracting patches %s - %s for %d images.\n', ...
  imdb.name, featsname, numel(impaths));
status = utls.textprogressbar(numel(impaths), 'startmsg', ...
  sprintf('Patch Extr. '), 'updatestep', 1);
for di = 1:numel(impaths)
  status(di);
  imname = imnames{di};
  respath = fullfile(patches_dir, [imname, opts.imgExt]);
  if exist(respath, 'file') == 2 && ~opts.override, continue; end
  
  [found, imi] = ismember(imname, {imdb.images.name});
  if ~found, error('Detections %s not found.', imname); end;
  if opts.grayscale
    im = utls.imread_grayscale(imdb.images(imi).path);
  else
    im = imread(dset.images(imi).path);
  end
  feats = utls.features_load(fullfile(dets_path, imname))';
  frames = feats.frames;
  if size(frames, 2) > opts.maxNumFeatures
    warning('Too many detected frames (%d) in %s, taking a random %d.\n', ...
      size(frames, 2), fullfile(dets_path, imname), opts.maxNumFeatures);
    frames = vl_colsubset(frames, opts.maxNumFeatures);
  end
  assert(isfield(feats, 'frames'), 'Invalid features %s - no geom. frames', ...
    dets_path);
  patches = opts.extractPatchesFun(im, frames, ...
    'scalingFactor', opts.scalingFactor, varargin{:});
  
  utls.patches_save(patches, respath, opts.scalingFactor);
end

end