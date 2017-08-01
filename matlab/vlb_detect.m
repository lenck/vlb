function vlb_detect(imdb, detector, varargin)
opts.override = false;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detector = det.detfactory(detector, varargin{:});

impaths = {imdb.images.path};
imnames = {imdb.images.name};
dest_dir = vlb_path('dets', imdb, detector);
vl_xmkdir(dest_dir);

fprintf('Computing detections %s for %d images.\n', ...
  detector.name, numel(impaths));
status = utls.textprogressbar(numel(impaths), 'startmsg', ...
  sprintf('Computing %s ', detector.name), 'updatestep', 1);
for si = 1:numel(impaths)
  impath = impaths{si};
  imname = imnames{si};
  det_path = fullfile(dest_dir, [imname, '.csv']);
  if exist(det_path, 'file') == 2 && ~opts.override
    status(numel(impaths));
    continue;
  end
  im = imread(impath);
  frames = detector.fun(im);
  frames = vl_frame2oell(frames);
  dlmwrite(det_path, frames', ';');
  status(si);
end

end
