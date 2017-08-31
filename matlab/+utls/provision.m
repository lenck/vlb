function downloaded = provision( url, tgt_dir, varargin )
opts.doneName = '.download.done';
opts.override = false;
opts = vl_argparse(opts, varargin);

downloaded = false;
done_file = fullfile(tgt_dir, opts.doneName);
if ~exist(tgt_dir, 'dir'), mkdir(tgt_dir); end
if exist(done_file, 'file') && ~opts.override, return; end;
unpack(url, tgt_dir);
downloaded = true;
create_done(done_file);
end

function create_done(done_file)
f = fopen(done_file, 'w'); fclose(f);
fprintf('To reprovision, delete %s.\n', done_file);
end

function unpack(url, tgt_dir)
[~,~,ext] = fileparts(url);
fprintf(isdeployed+1, ...
  'Downloading %s -> %s, this may take a while...\n',...
  url, tgt_dir);
switch ext
  case {'.tar', '.gz'}
    untar(url, tgt_dir);
  case '.zip'
    unzip(url, tgt_dir);
  otherwise
    error('Unknown archive %s', ext);
end
end