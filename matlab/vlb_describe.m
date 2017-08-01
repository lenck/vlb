function vlb_describe(imdb, detector, descriptor, varargin)

opts.imgExt = '.png';
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detector = det.detfactory(detector, varargin{:});
descriptor = desc.descfactory(descriptor, varargin{:});

patches_dir = vlb_path('patches', imdb, detector);
assert(isdir(patches_dir), 'Cannot find patches for %s - %s', ...
  imdb.name, detector.name);
pfiles = dir(fullfile(patches_dir, ['*', opts.imgExt]));
pfiles = arrayfun(@(a) fullfile(patches_dir, a.name), pfiles, 'Uni', false);

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
  patches = utls.patches_load(pfile);
  x = descriptor.fun(patches);
  dlmwrite(desc_path, x', ';');
  status(si);
end

end
