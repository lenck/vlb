function res = tcdet(img, varargin)
% Dependecies in Python: tensorflow, scikit-image, opencv-python

opts.url = 'https://codeload.github.com/ColumbiaDVMM/Transform_Covariant_Detector/zip/master';
opts.rootDir = fullfile(vlb_path('vendor'), 'tcdet');
[opts, varargin] = vl_argparse(opts, varargin);
opts.binDir = fullfile(opts.rootDir, 'Transform_Covariant_Detector-master/');
opts.netsDir = fullfile(opts.binDir, 'tensorflow_model');
opts.runDir = fullfile(opts.binDir, 'tensorflow');
[opts, varargin] = vl_argparse(opts, varargin);
opts.point_number = 1000;
opts = vl_argparse(opts, varargin);

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
cmd = sprintf('python tcdet_eval.py "%s" --save_feature "%s"', imname, featsname);
actpath = pwd;
try
  cd(opts.runDir);
  [ret, out] = system(cmd);
  [res.frames, res.detresponses] = tcdet_rundet(img, featsname);
catch 
  cd(actpath);
end
cd(actpath);
if ret ~= 0
  error('Error running TCDET python script.\n%s', out);
end
res.frames(1:2,:) = bsxfun(@minus, res.frames(1:2,:), padding');
res.frames(:, res.frames(1,:) < 0 | res.frames(2,:) < 0) = [];
res.frames(:, res.frames(1,:) > imsz(2) | res.frames(2,:) > imsz(1)) = [];

delete(imname);
delete(featsname);

end