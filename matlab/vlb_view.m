function res = vlb_view(cmd, varargin)

vlb_setup();
usage = @(varargin) utls.helpbuilder(varargin{:}, 'name', 'vlb_view');

cmds = struct();
cmds.patches = struct('fun', @view_patches, 'help', 'imdb feats imnum');
cmds.detections = struct('fun', @view_detections, 'help', 'imdb feats imnum');
cmds.detout = struct('fun', @view_detout, 'help', 'detector image');
cmds.matchpair = struct('fun', @view_matchpair, 'help', 'imdb tasknum');
cmds.matches = struct('fun', @view_matches, 'help', 'benchFun imdb feats tasknum');
cmds.sequencescores = struct('fun', @view_sequencescores, 'help', 'benchFun imdb feats sequence valuename');
cmds.descmatchpr = struct('fun', @view_descmatchpr, 'help', 'benchFun imdb feats tasknum');

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

function feats = view_detections(imdb, featsname, imid, varargin)
imdb = dset.factory(imdb);
feats_path = vlb_path('features', imdb, featsname);
if ~exist(feats_path, 'dir')
  error('No detections in %s.', feats_path);
end
if nargin < 3, error('Imid not specified.'); end;
imid = dset.utls.getimid(imdb, imid);
imname = imdb.images(imid).name;
feats = utls.features_load(fullfile(feats_path, imname));
if nargout == 0
  imshow(imdb.images(imid).path); hold on;
  if isfield(feats, 'scalingFactor')
    mframes = utls.frame_magnify_scale(feats.frames, feats.scalingFactor);
    vl_plotframe(mframes, 'LineWidth', 1, 'LineStyle', ':', 'Color', 'y', ...
      varargin{:});
  end
  vl_plotframe(feats.frames, 'LineWidth', 1, varargin{:});
  if isfield(feats, 'scalingFactor')
    legend('Measuerement region', 'Detection');
  end
end
end

function feats = view_detout(det, img, varargin)
det = features.factory('det', det, varargin{:});
feats = det.fun(img);
imshow(img); hold on;
vl_plotframe(feats.frames, 'LineWidth', 1);
end



function res = view_patches(imdb, featsname, imid, varargin)
imdb = dset.factory(imdb);
patches_path = vlb_path('patches', imdb, featsname);
if ~exist(patches_path, 'dir')
  error('No patches in %s.', patches_path);
end
if nargin < 3, error('Imid not specified.'); end
imid = dset.utls.getimid(imdb, imid);
imname = imdb.images(imid).name;
res = utls.patches_load(fullfile(patches_path, [imname, '.png']));
if nargout == 0
  imshow(vl_imarray(squeeze(res)));
end
end




function view_matchpair(imdb, taskid, varargin)
opts.imperrow = ceil(sqrt(numel(taskid)));
opts = vl_argparse(opts, varargin);
imdb = dset.factory(imdb);
clf;

if numel(taskid) == 1 % Show a single pair
  task = imdb.tasks(taskid);
  imaid = dset.utls.getimid(imdb, task.ima);
  ima = imread(imdb.images(imaid).path);
  imbid = dset.utls.getimid(imdb, task.imb);
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
else % show multiple pairs
  ncols = opts.imperrow;
  nrows = ceil(numel(taskid)/ncols);
  for ti = 1:numel(taskid)
    [col, row] = ind2sub([ncols, nrows], ti);
    task = imdb.tasks(taskid(ti));
    imaid = dset.utls.getimid(imdb, task.ima);
    ima = imread(imdb.images(imaid).path);
    imbid = dset.utls.getimid(imdb, task.imb);
    imb = imread(imdb.images(imbid).path);
    vl_tightsubplot(nrows, ncols, col + (row-1)*ncols, 'margin', 0.01);
    imshow(imfuse(ima, imb, 'montage'), 'border', 'tight');
    text(0, 0, sprintf('%s -> %s', imdb.images(imaid).name, ...
      imdb.images(imbid).name), 'Interpreter', 'none', ...
      'BackgroundColor', 'k', 'Color', 'g');
  end
end
end




function res = view_matches(benchname, imdb, featsname, taskid, varargin)
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
  imaid = dset.utls.getimid(imdb, task.ima);
  imbid = dset.utls.getimid(imdb, task.imb);
  
  subplot(1,2,1);
  imshow(imdb.images(imaid).path); hold on;

  vl_plotframe(res.geom.ella, 'LineWidth', 1, 'Color', [0.1 0.1 0.1]);
  vl_plotframe(res.geom.ellb_rep, 'LineWidth', 1, 'Color', [0.3 0 0.3]);
  vl_plotframe(res.geom.ellb_rep(:, res.matches(1, res.matches~=0)), 'LineWidth', 1, 'Color', 'yellow');
  vl_plotframe(res.geom.ella(:, res.matches~=0), 'LineWidth', 2, 'Color', 'green');
  title(['IM-A ', featsname], 'Interpreter', 'none');
  
  subplot(1,2,2);
  imshow(imdb.images(imbid).path); hold on;
  
  la = [];
  la(end+1) = vl_plotframe(res.geom.ellb, 'LineWidth', 1, 'Color', [0.1 0.1 0.1]);
  la(end+1) = vl_plotframe(res.geom.ella_rep, 'LineWidth', 1, 'Color', [0.3 0 0.3]);
  la(end+1) = vl_plotframe(res.geom.ella_rep(:, res.matches~=0), 'LineWidth', 1, 'Color', 'yellow');
  la(end+1) = vl_plotframe(res.geom.ellb(:, res.matches(1, res.matches~=0)), 'LineWidth', 2, 'Color', 'green');
  title(['IM-B ' featsname], 'Interpreter', 'none');
  legend(la, 'Valid', 'Reproj', 'Matched-Reproj.', 'Matched-Detected');
end
end


function res_f = view_sequencescores(benchName, imdb, featsname, sequence, valuename, varargin)
imdb = dset.factory(imdb);
assert(ismember(benchName, {'detrep', 'detmatch'}), 'Unsupported benchmark.');
if ~iscell(featsname), featsname = {featsname}; end;

res = cell(numel(featsname), 1);
for fi = 1:numel(featsname)
  scoresdir = vlb_path('scores', imdb, featsname{fi}, benchName);
  scores_path = fullfile(scoresdir, 'results.csv');
  if ~exist(scores_path, 'file')
    error('Scores file %s does not exist.', scores_path);
  end;
  res{fi} = readtable(scores_path, 'Delimiter', ',');
end
res = vertcat(res{:});
res_f = res(ismember(res.sequence, sequence), :);

if nargout == 0
  for fi = 1:numel(featsname)
    plot(res_f{ismember(res_f.features, featsname{fi}), valuename}, varargin{:});
    hold on;
  end;
  xlabel('Image'); ylabel(valuename); grid on;
end
end


function res = view_descmatchpr(imdb, featsname, taskid, varargin)
imdb = dset.factory(imdb);
assert(taskid > 0 && taskid < numel(imdb.tasks), 'Invalid Task ID');
if ~iscell(featsname), featsname = {featsname}; end;

res = cell(numel(featsname), 1);
info = cell(numel(featsname), 1);
for fi = 1:numel(featsname)
  scoresdir = vlb_path('scores', imdb, featsname{fi}, 'descmatch');
  scores_path = fullfile(scoresdir, 'results.csv');
  info_path = fullfile(scoresdir, 'results.mat');
  if ~exist(scores_path, 'file')
    error('Scores file %s does not exist.', scores_path);
  end;
  res{fi} = readtable(scores_path, 'Delimiter', ',');
  in = load(info_path); in = in.info;
  assert(numel(in) == numel(imdb.tasks), 'Invalid results.');
  info{fi} = in(taskid);
end
res = vertcat(res{:}); info = vertcat(info{:});

if nargout == 0
  for fi = 1:numel(featsname)
    plot(info(fi).recall, info(fi).precision);
    hold on;
  end;
  xlabel('Recall'); ylabel('Precision'); grid on;
  title(sprintf('%s -> %s', imdb.tasks(taskid).ima, imdb.tasks(taskid).imb));
end
end