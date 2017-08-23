function features = features_load( path, varargin )
%FEATURES_Load Load a features structure at the specified path
opts.checkonly = false;
opts = vl_argparse(opts, varargin);

features = struct();
files = dir([path, '.*.*']);
if isempty(files), features = []; return; end;

for fi = 1:numel(files)
  [~, fname, ext] = fileparts(files(fi).name);
  fname = strsplit(fname, '.');
  assert(numel(fname) == 2, 'Invalid features file name %s', files(fi).name);
  field = fname{2};
  fpath = [path, '.', field, ext];
  if opts.checkonly
    features.(field) = nan;
  else
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
    end
  end
end

end

