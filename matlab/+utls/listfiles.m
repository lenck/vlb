function files = listfiles(path, varargin)
opts.keepext = true;
opts.fullpath = true;
opts = vl_argparse(opts, varargin);

files = dir(path);
if isempty(files), files = {}; return; end;
is_valid = ~[files.isdir] & arrayfun(@(d) d.name(1)~='.', files)';
files = {files.name};
files = files(is_valid);
if ~opts.keepext
  for fi = 1:numel(files), [~, files{fi}, ~] = fileparts(files{fi}); end;
end
if opts.fullpath
  files = cellfun(@(a) fullpath(path, a), files, 'Uni', false);
end
end