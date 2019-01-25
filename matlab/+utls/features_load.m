function features = features_load( path, varargin )
%FEATURES_Load Load a features structure at the specified path
opts.checkonly = false;
opts.compulsoryFields = {};
opts = vl_argparse(opts, varargin);

features = struct();
files = dir([path, '.*.*']);
if isempty(files), features = []; return; end
% Check whether all required fields are present
if ~isempty(opts.compulsoryFields)
  [~, imname] = fileparts(path);
  compulsoryFnames = cellfun(@(cf) [imname, '.', cf], ...
    opts.compulsoryFields, 'Uni', false);
  if any(~ismember(compulsoryFnames, {files.name}))
     features = []; return;
  end
end

for fi = 1:numel(files)
  [~, fname, ext] = fileparts(files(fi).name);
  fname = strsplit(fname, '.');
  assert(numel(fname) == 2, 'Invalid features file name %s', files(fi).name);
  field = fname{2};
  fpath = [path, '.', field, ext];
  if opts.checkonly
    features.(field) = nan;
  else
    fp = dir(fpath);
    if fp.bytes == 0
      features.(field) = [];
      continue;
    end
    switch ext
      case '.csv'
        features.(field) = dlmread(fpath, ';')';
      case '.txt'
        fd = fopen(fpath, 'r');
        data = textscan(fd, '%s');
        features.(field) = data{1}{1};
        fclose(fd);
      case '.mat'
        data = load(fpath);
        features.(field) = data.data;
      case '.oxf' % Oxford frames format (1.\nNFEATS\nx y a b c\n)
        features.(field) = legacy.vgg_frames_read(fpath);
    end
  end
end

end

