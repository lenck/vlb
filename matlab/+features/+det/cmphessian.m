function res = cmphessuan(img, varargin)
% localFeatures.CmpHessian CMP Hessian Affine wrapper
%   localFeatures.CmpHessian() constructs new wrapper object of a binary
%   created by compilation of a source code available at:
%   http://cmp.felk.cvut.cz/~perdom1/code/hesaff.tar.gz
%
%   This detector has a dependency in OpenCV library.
%
%   (No options currently available)
%
%   See also: helpers.OpenCVInstaller

% Authors: Karel Lenc

% AUTORIGHTS

BinPath = fullfile(fileparts(mfilename('fullpath')), 'hesaff');
opts = struct(...
  'threshold', -1,...
  'max_iter', -1,...
  'desc_factor', 5.2,...
  'patch_size', -1, ...
  'rot_invariant', -1,...
  'aff_invariant', -1,...
  'fast_norm',-1,...
  'verbose',-1 ...
  );
opts = vl_argparse(opts, varargin);

res.detName = sprintf('cmphessian');
if isempty(img), res.frames = zeros(6, 0); res.descriptors = []; return; end;

tmpName = tempname;
imgFile = [tmpName '.pgm'];
featFile = [tmpName '.pgm.hes.sift'];

imwrite(img,imgFile);
args = ' -v -k 2';
fields = fieldnames(opts);
for i = 1:numel(fields)
  val = opts.(fields{i});
  if val >= 0
    args = [args,' --',fields{i},' ', num2str(val)];
  end
end

args = [args sprintf(' -i "%s" ',imgFile)];
cmd = [ BinPath ' ' args];
[status,msg] = system(cmd);
if status
  error('%d: %s: %s', status, cmd, msg) ;
end

res = readFeaturesAffDeNormFile(featFile);
delete(featFile); delete(imgFile);

res.frames = utls.frame_magnify_scale(res.frames, 1./opts.desc_factor);
end

function [res] = readFeaturesAffDeNormFile(featuresFile, varargin)
% READFEATURESFILE Read file exported by some of the older frame detectors.
%   FRAMES = READFEATURESFILE(FRAME_FILE_PATH) Reads FRAMES from a file
%   defined by FRAME_FILE_PATH
%
%   vl_ubcread cannot be used because some older detectors produce files
%   which contain length of the descriptors = 1 which the vl_ubcread function
%   is not able to handle.
%
% Function accepts the following options:
%   'FloatDesc' ::
%      Feature file contains floating point descriptors.
%

% Authors: Karel Lenc

% AUTORIGHTS
import helpers.*;
opts.floatDesc = false;
opts = vl_argparse(opts, varargin);

fid = fopen(featuresFile,'r');
if fid==-1
  error('Could not read file: %s\n',featuresFile);
end
[header,count] = fscanf(fid,'%f',2);
if count~= 2
  fclose(fid);
  error('Invalid data format, could not parse file %s\n',featuresFile);
end
descrLen = header(1);
numFeatures = header(2);
frames = zeros(8,numFeatures);
if descrLen == 0 || descrLen == 1
  [frames,count] = fscanf(fid,'%f',[7 numFeatures]);
  if count~=5*numFeatures
    fclose(fid);
    error('Invalid data format, could not parse file  %s\n',featuresFile);
  end
else
  descriptors = zeros(descrLen,numFeatures);
  for k = 1:numFeatures
    [frames(:,k), count] = fscanf(fid, '%f', [1 8]);
    if count ~= 8
      fclose(fid);
      error('Invalid data format, (parsing feature %d, frame)',k);
    end
    if opts.floatDesc
      [descriptors(:,k), count] = fscanf(fid, '%f', [1 descrLen]);
    else
      [descriptors(:,k), count] = fscanf(fid, '%d', [1 descrLen]);
    end
    if count ~= descrLen
      fclose(fid);
      error('Invalid data format, could not parse file (parsing feature %d, descriptor)',k);
    end
  end
end
fclose(fid);
res.type = frames(1,:);
res.detresponse = frames(2,:);
res.frames = frames(3:end,:);
res.frames(1:2,:) = res.frames(1:2,:) + 1; % Convert to Matlab coordinates

end
