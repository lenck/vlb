function vlb_detdesc(imdb, detdesc, varargin)
import features.*;

opts.override = false;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detdesc = features.factory('detdesc', detdesc, varargin{:});

impaths = {imdb.images.path};
dets_dir = vlb_path('dets', imdb, detector);
vl_xmkdir(dets_dir);
descs_dir = vlb_path('descs', imdb, detdesc, detdesc);
vl_xmkdir(descs_dir);

fprintf('Computing detections and descriptor %s for %d patch images.\n', ...
  detdesc.name, numel(impaths));
status = utls.textprogressbar(numel(impaths), 'startmsg', ...
  sprintf('Computing %s ', descriptor.name), 'updatestep', 1);
for si = 1:numel(impaths)
  impath = impaths{si};
  [~, imname, ~] = fileparts(impath);
  det_path = fullfile(dets_dir, [imname, '.csv']);
  info_path = fullfile(dets_dir, [imname, '.mat']);
  desc_path = fullfile(descs_dir, [imname, '.csv']);
  if exist(det_path, 'file') == 2 && exist(info_path, 'file') == 2 && ...
      exist(desc_path, 'file') == 2 && ~opts.override
    status(numel(impaths));
    continue;
  end
  [f,d,info] = detdesc.fun(patches);
  dlmwrite(det_path, f', ';');
  dlmwrite(desc_path, d', ';');
  save(info_path, 'info');
  status(si);
end

end
