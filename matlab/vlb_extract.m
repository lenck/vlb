function vlb_extract(imdb, detector, varargin)

opts.method = @utls.extract_patches_covdet;
opts.override = false;
opts.grayscale = true;
opts.imgExt = '.png';
opts.scalingFactor = 5;
opts.extractPatchesFun = @utls.patches_extract_covdet;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detector = features.factory('det', detector, varargin{:});

dets_path = vlb_path('dets', imdb, detector);
assert(isdir(dets_path), 'Cannot find detections for %s - %s', ...
  imdb.name, detector.name);
detf = utls.listfilesdir(fullfile(dets_path, '*.csv'));

patches_dir = vlb_path('patches', imdb, detector);
vl_xmkdir(patches_dir);

fprintf('Extracting patches %s - %s for %d images.\n', ...
  imdb.name, detector.name, numel(detf));
status = utls.textprogressbar(numel(detf), 'startmsg', ...
  sprintf('Patch Extr. '), 'updatestep', 1);
for di = 1:numel(detf)
  status(di);
  [~, name, ~] = fileparts(detf{di});
  respath = fullfile(patches_dir, [name, opts.imgExt]);
  if exist(respath, 'file') == 2 && ~opts.override
    continue;
  end
  
  [found, imi] = ismember(name, {imdb.images.name});
  if ~found, error('Detections %s not found.', name); end;
  if opts.grayscale
    im = utls.imread_grayscale(imdb.images(imi).path);
  else
    im = imread(dset.images(imi).path);
  end
  frames = dlmread(fullfile(dets_path, [name, '.csv']))';
  patches = opts.extractPatchesFun(im, frames, ...
    'scalingFactor', opts.scalingFactor, varargin{:});
  
  utls.patches_save(patches, respath);
end

end