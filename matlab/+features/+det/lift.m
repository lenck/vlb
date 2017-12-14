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
featsname = [name, '.txt'];

cmd = sprintf('%s compute_detector.py "%s" "%s" "%s" 0 1 0 "%s" %d', ...
  opts.pythoncmd, ...
  opts.confPath, imname, featsname, opts.modelPath, opts.numKeypoints);
utls.sysrun(cmd, 'runDir', opts.pythonDir, varargin{:});
res = frames_read(featsname);
delete(imname);
delete(featsname);
end


function [out] = frames_read(framesFile)
fid = fopen(framesFile, 'r');
if fid==-1, error('Could not read file: %s\n', framesFile); end
[header, count] = fscanf(fid, '%f', 2);
if count ~= 2
  fclose(fid);
  error('Invalid frames format.');
end
numPoints = header(2);
[data, count] = fscanf(fid,'%f', [13, numPoints]);
fclose(fid);
if count ~= 13 * numPoints, error('Invalid frames format.'); end
% Transform the frame properly
% X Y CORNERNESS SCALE/3 ANGLE TYPE LAP EXTR M11 M12 M21 M22
out.frames = zeros(4, numPoints);
out.frames(1:2,:) = data(1:2,:) + 1;
out.frames(3:4,:) = data(3:4, :);
out.detresponses = data(5, :);
end