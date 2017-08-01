function res = vlb_view(cmd, varargin)

vlb_setup();
usage = @(varargin) utls.helpbuilder(varargin{:}, 'name', 'vlb_view');

cmds = struct();
cmds.patches = struct('fun', @view_patches, 'help', 'imdb det imnum');
cmds.detections = struct('fun', @view_detections, 'help', 'imdb det imnum');

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


function res = view_detections(imdb, detector, imid, varargin)
imdb = dset.dsetfactory(imdb);
[detector, varargin] = det.detfactory(detector, varargin{:});
dets_path = vlb_path('dets', imdb, detector);
if ~exist(dets_path, 'dir')
  error('No detections in %s.', dets_path);
end
if nargin < 3, error('Imid not specified.'); end;
imid = getimid(imdb, imid);
imname = imdb.images(imid).name;
res = dlmread(fullfile(dets_path, [imname, '.csv']), ';')';
if nargout == 0
  imshow(imdb.images(imid).path); hold on;
  vl_plotframe(res, 'LineWidth', 1, varargin{:});
end
end

function res = view_patches(imdb, detector, imid, varargin)
imdb = dset.dsetfactory(imdb);
detector = det.detfactory(detector, varargin{:});
patches_path = vlb_path('patches', imdb, detector);
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