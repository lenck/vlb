function res = lift(img, varargin)
% Dependecies in Python: see vendor/lift/depdendecies.txt + opencv-python

opts.url = 'https://github.com/cvlab-epfl/LIFT/archive/master.zip';
opts.rootDir = fullfile(vlb_path('vendor'), 'lift');
[opts, varargin] = vl_argparse(opts, varargin);
opts.binDir = fullfile(opts.rootDir, 'LIFT-master');
[opts, varargin] = vl_argparse(opts, varargin);
opts.pythonDir = fullfile(opts.binDir, 'python-code');
opts.ccodeDir = fullfile(opts.binDir, 'c-code');
opts.confPath = fullfile(opts.binDir, '/models/configs/picc-finetune-nopair.config');
opts.modelPath = fullfile(opts.binDir, '/models/picc-best/');
opts.numKeypoints = 2000;
opts.pythoncmd = 'python3';
[opts, varargin] = vl_argparse(opts, varargin);

res.detName = 'lift'; res.args = opts; res.frames = zeros(5, 0);
if isempty(img), return; end

utls.provision(opts.url, opts.rootDir, 'forceExt', '.zip');

name = tempname;
imname = [name, '.png'];
imwrite(img, imname);
featsname = [name, '.mat'];

scriptPath = fullfile(vlb_path, 'matlab', '+features', '+utls', 'tcdet_eval.py');
copyfile(scriptPath, opts.runDir);
scriptPath = fullfile(vlb_path, 'matlab', '+features', '+utls', 'tcdet_rundet.m');
copyfile(scriptPath, opts.runDir);

cmd = sprintf('%s tcdet_eval.py "%s" --save_feature "%s"', opts.pythoncmd, imname, featsname);
utls.sysrun(cmd, 'runDir', opts.runDir, varargin{:});

actpath = pwd;
try
  cd(opts.runDir);
  [res.frames, res.detresponses] = tcdet_rundet(img, featsname, ...
    opts.point_number, opts.thr);
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