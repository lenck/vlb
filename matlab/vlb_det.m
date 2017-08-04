function vlb_det(imdb, detector, varargin)
import features.*;

opts.override = false;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detector = features.factory('det', detector, varargin{:});

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
  det_info_path = fullfile(dest_dir, [imname, '.mat']);
  if exist(det_path, 'file') == 2 && ...
      exist(det_info_path, 'file') == 2 && ~opts.override
    status(numel(impaths)); continue;
  end
  im = imread(impath);
  [frames, info] = detector.fun(im);
  frames = vl_frame2oell(frames);
  dlmwrite(det_path, frames', ';');
  save(det_info_path, 'info');
  status(si);
end

end
