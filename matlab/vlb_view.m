function res = vlb_view(cmd, varargin)

vlb_setup();
usage = @(varargin) utls.helpbuilder(varargin{:}, 'name', 'vlb_view');

cmds = struct();
cmds.patches = struct('fun', @view_patches, 'help', 'imdb feats imnum');
cmds.detections = struct('fun', @view_detections, 'help', 'imdb feats imnum');
cmds.matches = struct('fun', @view_matches, 'help', 'imdb feats tasknum');
cmds.matchpair = struct('fun', @view_matchpair, 'help', 'imdb tasknum');

% The last command is always help
cmds.help = struct('fun', @(varargin) usage(cmds, '', varargin{:}));
if nargin < 1, cmd = nan; end;
if ~ischar(cmd), usage(cmds); return; end
if strcmp(cmd, 'commands'), res = cmds; return; end;

if isfield(cmds, cmd) && ~isempty(cmds.(cmd).fun)
  if nargout == 1
    res = cmds.(cmd).fun(varargin{:});
  else
    cmds.(cmd).fun(varargin{:});
  end
else
  error('Invalid command. Run help for list of valid commands.');
end

end

function imid = getimid(imdb, imid)
if ischar(imid)
  imname = imid;
  [found, imid] = ismember(imname, {imdb.images.name});
  if ~found, error('Image %s not found.', imname); end;
end
if imid > numel(imdb.images) || imid < 1
  error('Invalid image id %d.', imid);
end
end


function feats = view_detections(imdb, featsname, imid, varargin)
imdb = dset.factory(imdb);
feats_path = vlb_path('features', imdb, featsname);
if ~exist(feats_path, 'dir')
  error('No detections in %s.', feats_path);
end
if nargin < 3, error('Imid not specified.'); end;
imid = getimid(imdb, imid);
imname = imdb.images(imid).name;
feats = utls.features_load(fullfile(feats_path, imname));
if nargout == 0
  imshow(imdb.images(imid).path); hold on;
  vl_plotframe(feats.frames, 'LineWidth', 1, varargin{:});
end
end

function res = view_patches(imdb, featsname, imid, varargin)
imdb = dset.factory(imdb);
patches_path = vlb_path('patches', imdb, featsname);
if ~exist(patches_path, 'dir')
  error('No patches in %s.', patches_path);
end
if nargin < 3, error('Imid not specified.'); end;
imid = getimid(imdb, imid);
imname = imdb.images(imid).name;
res = utls.patches_load(fullfile(patches_path, [imname, '.png']));
if nargout == 0
  imshow(vl_imarray(res));
end
end


function res = view_matches(imdb, featsname, benchname, taskid, varargin)
imdb = dset.factory(imdb);
scoresdir = vlb_path('scores', imdb, featsname, benchname);
info_path = fullfile(scoresdir, 'results.mat');
feats_path = vlb_path('features', imdb, featsname);

if ~exist(info_path, 'file')
  error('Could not find benchamrk results in %s.', info_path);
end
if taskid < 1 || taskid > numel(imdb.tasks)
  error('Invalid task id %d', taskid);
end

res = load(info_path);
res = res.info(taskid);
if nargout == 0
  task = imdb.tasks(taskid);
  imaid = getimid(imdb, task.ima);
  featsa = utls.features_load(fullfile(feats_path, imdb.images(imaid).name));
  imbid = getimid(imdb, task.imb);
  featsb = utls.features_load(fullfile(feats_path, imdb.images(imbid).name));
  
  subplot(1,2,1);
  imshow(imdb.images(imaid).path); hold on;

  vl_plotframe(featsa.frames, 'LineWidth', 1, 'Color', [0.1 0.1 0.1]);
  vl_plotframe(featsa.frames(:, res.fa_valid), 'LineWidth', 1, 'Color', 'blue');
  vl_plotframe(res.ellb_rep(:, res.matches(1, res.matches~=0)), 'LineWidth', 1, 'Color', 'yellow');
  vl_plotframe(res.ella(:, res.matches~=0), 'LineWidth', 2, 'Color', 'green');
  title('IM-A');
  
  subplot(1,2,2);
  imshow(imdb.images(imbid).path); hold on;
  
  la = zeros(4, 1);
  la(1) = vl_plotframe(featsb.frames, 'LineWidth', 1, 'Color', [0.1 0.1 0.1]);
  la(2) = vl_plotframe(featsb.frames(:, res.fb_valid), 'LineWidth', 1, 'Color', 'blue');
  la(3) = vl_plotframe(res.ella_rep(:, res.matches~=0), 'LineWidth', 1, 'Color', 'yellow');
  la(4) = vl_plotframe(res.ellb(:, res.matches(1, res.matches~=0)), 'LineWidth', 2, 'Color', 'green');
  title('IM-B');
  legend(la, 'Detected', 'Valid', 'Matched-Reproj.', 'Matched-Detected');
end
end


function view_matchpair(imdb, taskid, varargin)
imdb = dset.factory(imdb);

task = imdb.tasks(taskid);
imaid = getimid(imdb, task.ima);
ima = imread(imdb.images(imaid).path);
imbid = getimid(imdb, task.imb);
imb = imread(imdb.images(imbid).path);

switch imdb.geometry
  case 'homography'
    subplot(2,2,1); imshow(ima); title('A');
    subplot(2,2,2); imshow(imb); title('B');
    task = imdb.tasks(taskid);
    H = task.H;
    [imb_w, ref_b, ref_a] = utls.warpim_H(imb, H, 'invert', false);
    resim_a = imfuse(ima, ref_a, imb_w, ref_b, 'falsecolor', ...
      'Scaling', 'joint', 'ColorChannels', [1 2 0]);
    subplot(2,2,3); imshow(resim_a);  title('B \rightarrow A');
    
    [ima_w, ref_a, ref_b] = utls.warpim_H(ima, H, 'invert', true);
    resim_b = imfuse(imb, ref_b, ima_w, ref_a, 'falsecolor', ...
      'Scaling', 'joint', 'ColorChannels', [1 2 0]);
    subplot(2,2,4); imshow(resim_b); title('A \rightarrow B');
  otherwise
    error('Unsupported geometry: `%s`', imdb.geometry);
end
  
end