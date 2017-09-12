function res = tcdet(img, varargin)
% Dependecies in Python: tensorflow, scikit-image, opencv-python

opts.url = 'https://codeload.github.com/ColumbiaDVMM/Transform_Covariant_Detector/zip/master';
opts.rootDir = fullfile(vlb_path(), 'data', 'tcdet');
[opts, varargin] = vl_argparse(opts, varargin);
opts.binDir = fullfile(opts.rootDir, 'Transform_Covariant_Detector-master/');
opts.netsDir = fullfile(opts.binDir, 'tensorflow_model');
opts.runDir = fullfile(opts.binDir, 'tensorflow');
[opts, varargin] = vl_argparse(opts, varargin);
opts.point_number = 1000;
opts = vl_argparse(opts, varargin);

res.detName = 'tcdet'; res.args = opts;
if isempty(img), res.frames = zeros(5, 0); return; end;

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
  res.frames = tcdet_rundet(img, featsname);
catch 
  cd(actpath);
end
cd(actpath);
if ret ~= 0
  error('Error running TCDET python script.\n%s', out);
end

delete(imname);
delete(featsname);

end