function ungzip( src, tgt_dir )
%UNGZIP Unpack raw .gz file (not .tar.gz)

[~, filename, ext] = fileparts(src);
assert(strcmp(ext, '.gz'), 'Not a .GZ file.');
assert(~strcmp(filename(end-3:end), '.tar'), 'Invalid use on .tar.gz file.');
gzTgtPath = fullfile(tgt_dir, [filename, ext]);
if strcmp(src(1:7), 'http://')
  websave(gzTgtPath, src);
else
  assert(exist(src, 'file') == 2, 'File %s does not exist', src);
  copyfile(src, gzTgtPath);
end

curDir = pwd;
cd(tgt_dir)
[status, ret] = system(sprintf('gunzip %s', gzTgtPath));
cd(curDir);
if status ~= 0
  delete(gzTgtPath);
  error('Error unpacking %s: %s', src, ret);
end

end

