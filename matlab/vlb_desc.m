function vlb_desc(imdb, detector, descriptor, varargin)
import features.*;

opts.imgExt = '.png';
opts.override = false;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detector = features.factory('det', detector, varargin{:});
descriptor = features.factory('desc', descriptor, varargin{:});

switch descriptor.describes
  case 'patches'
    describe_patches(imdb, detector, descriptor, opts);
  case 'frames'
    describe_frames(imdb, detector, descriptor, opts);
end

end

function describe_patches(imdb, detector, descriptor, opts)

patches_dir = vlb_path('patches', imdb, detector);
assert(isdir(patches_dir), 'Cannot find patches for %s - %s', ...
  imdb.name, detector.name);
pfiles = utls.listfilesdir(fullfile(patches_dir, ['*', opts.imgExt]));

dest_dir = vlb_path('descs', imdb, detector, descriptor);
vl_xmkdir(dest_dir);

fprintf('Computing descriptor %s for %d patch images.\n', ...
  descriptor.name, numel(pfiles));
status = utls.textprogressbar(numel(pfiles), 'startmsg', ...
  sprintf('Computing %s ', descriptor.name), 'updatestep', 1);
for si = 1:numel(pfiles)
  pfile = pfiles{si};
  [~, imname, ~] = fileparts(pfile);
  desc_path = fullfile(dest_dir, [imname, '.csv']);
  if exist(desc_path, 'file') == 2 && ~opts.override
    status(numel(impaths));
    continue;
  end
  patches = utls.patches_load(pfile);
  x = descriptor.fun(patches);
  dlmwrite(desc_path, x', ';');
  status(si);
end

end


function describe_frames(imdb, detector, descriptor, opts)
% Has a pitfal in creating new detections - the testing must be adjusted.
dets_dir = vlb_path('dets', imdb, detector);
assert(isdir(dets_dir), 'Cannot find frames for %s - %s', ...
  imdb.name, detector.name);
dfiles = utls.listfilesdir(fullfile(dets_dir, '*.csv'));

dets_dest_dir = vlb_path('dets', imdb, [detector.name, '-', descriptor.name]);
desc_dest_dir = vlb_path('descs', imdb, detector, descriptor);
vl_xmkdir(desc_dir);

fprintf('Computing descriptor %s for %d set of of frames.\n', ...
  descriptor.name, numel(dfiles));
status = utls.textprogressbar(numel(dfiles), 'startmsg', ...
  sprintf('Computing %s ', descriptor.name), 'updatestep', 1);
for si = 1:numel(dfiles)
  ffile = dfiles{si};
  [~, imname, ~] = fileparts(pfile);
  dets_path = fullfile(dets_dest_dir, [imname, '.csv']);
  desc_path = fullfile(desc_dest_dir, [imname, '.csv']);
  if exist(dets_path, 'file') && exist(desc_path, 'file') == 2 && ~opts.override
    status(numel(impaths));
    continue;
  end
  frames = csvread(ffile, ';');
  [found, im_idx] = ismember(imname, {imdb.images.name});
  assert(found, 'Unable to find a dataset image for %s.', pfile);
  im = imread(imdb.images.path{im_idx});
  [fnew, dnew] = descriptor.fun(im, frames);
  dlmwrite(dets_path, fnew', ';');
  dlmwrite(desc_path, dnew', ';');
  status(si);
end

end

