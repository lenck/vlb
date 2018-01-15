function res = tcdet(img, varargin)
% Dependecies in Python: tensorflow, scikit-image, opencv-python, exifread

opts.url = 'https://codeload.github.com/ColumbiaDVMM/Transform_Covariant_Detector/zip/master';
opts.rootDir = fullfile(vlb_path('vendor'), 'tcdet');
[opts, varargin] = vl_argparse(opts, varargin);
opts.binDir = fullfile(opts.rootDir, 'Transform_Covariant_Detector-master/');
opts.netsDir = fullfile(opts.binDir, 'tensorflow_model');
opts.runDir = fullfile(opts.binDir, 'tensorflow');
[opts, varargin] = vl_argparse(opts, varargin);
opts.point_number = 4000;
opts.thr = 1.2;
[opts, varargin] = vl_argparse(opts, varargin);

res.detName = 'tcdet'; res.args = opts; res.frames = zeros(5, 0);
if isempty(img), return; end;

padding = [0, 0];
imsz = [size(img, 1), size(img, 2)];
if any(imsz < 105)
  padding = ceil(max(105 - imsz, 0) ./ 2);
  img = padarray(img, [padding, 0], 'replicate');
end

utls.provision(opts.url, opts.rootDir, 'forceExt', '.zip');

name = tempname;
imname = [name, '.png'];
imwrite(img, imname);
featsname = [name, '.mat'];

scriptPath = fullfile(vlb_path, 'matlab', '+features', '+utls', 'tcdet_eval.py');
copyfile(scriptPath, opts.runDir);
scriptPath = fullfile(vlb_path, 'matlab', '+features', '+utls', 'tcdet_rundet.m');
copyfile(scriptPath, opts.runDir);

cmd = sprintf('python2 tcdet_eval.py "%s" --save_feature "%s"', imname, featsname);
env = struct(); %env = struct('LD_LIBRARY_PATH', '/users/karel/anaconda3/lib');
[out, info] = utls.sysrun(cmd, 'runDir', opts.runDir, 'unset_ld', false, 'env', env, varargin{:});
res.dettime = info.time; 

actpath = pwd;
try
  cd(opts.runDir);
  [res.frames, res.detresponses, time] = tcdet_rundet(img, featsname, ...
    opts.point_number, opts.thr);
  if isfield(time, 'tftime') % Needs a hacked python_eval
    res.dettime = time.tftime;
  end
  res.dettime = res.dettime + time.dettime;
catch e
  cd(actpath);
  throw(e);
end
cd(actpath);

res.frames(1:2,:) = bsxfun(@minus, res.frames(1:2,:), padding');
res.frames(:, res.frames(1,:) < 0 | res.frames(2,:) < 0) = [];
res.frames(:, res.frames(1,:) > imsz(2) | res.frames(2,:) > imsz(1)) = [];

delete(imname);
delete(featsname);

end