function [ res ] = surf( img, feats, varargin )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


% Authors: Karel Lenc

% AUTORIGHTS
opts.rootDir = fullfile(vlb_path(), 'data', 'surf');
opts.binPath = fullfile(opts.rootDir,'SURF-V1.0.9','surf.ln');
opts.url = 'http://www.vision.ee.ethz.ch/~surf/SURF-V1.0.9.tar.gz';
[opts, varargin] = vl_argparse(opts, varargin);
res.args = opts;

utls.provision(opts.url, opts.rootDir);

surfopts = struct(...
  'thres', 1000,... % blob response threshold
  'ms', 3,...       % custom lobe size
  'ss', 2,...       % initial sampling step
  'oc', 4,...       % number of octaves
  'u', [],...    % U-SURF (not rotation invariant)
  'e',[],...      % extended descriptor (SURF-128)
  'in', 4);         % descriptor size
surfopts = vl_argparse(surfopts, varargin);


tmpName = tempname;
imagePath = [tmpName '.pgm']; imwrite(img, imagePath);
outFeaturesFile = [tmpName '.surf'];
args = buildArgs(surfopts, imagePath, outFeaturesFile);
if ~isempty(feats)
  framesPath = [tmpName '.frames'];
  legacy.vgg_features_write(framesPath, feats.frames, []);
  args = [args ' -p1 ', framesPath];
end
cmd = [opts.binPath ' ' args];
[status, msg] = system(cmd);
if status ~= 0, error('%d: %s: %s', status, cmd, msg); end
[res.frames, res.descs] = legacy.vgg_features_read(outFeaturesFile,'FloatDesc',true);
delete(outFeaturesFile);
delete(imagePath);
if ~isempty(feats), delete(framesPath); end;
end

function args = buildArgs(opts, imagePath, outFile)
% -nl - do not write the hessian keypoint type
args = sprintf('-nl -i "%s" -o "%s"', imagePath, outFile);
fields = fieldnames(opts);
for i = 1:numel(fields)
  val = opts.(fields{i});
  if ~isempty(val)
    if ismember(fields{i},{'u','e'})
      if val, args = [args,' -',fields{i}]; end
    else
      args = [args,' -',fields{i},' ', num2str(val)];
    end
  end
end
end