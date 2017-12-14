function [ out, info ] = sysrun( cmd, varargin )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
opts.gpu = [];
[opts, varargin] = vl_argparse(opts, varargin);
opts.unset_ld = isempty(opts.gpu); % Set true if segfaults, has to be false for CUDA
opts.runDir = pwd();
opts.verbose = false;
opts = vl_argparse(opts, varargin);

if ~isempty(opts.gpu)
  opts.gpu = cellfun(@num2str, opts.gpu - 1, 'Uni', false);
  opts.gpu = strjoin(opts.gpu, ',');
end
addcmd = '';
if opts.unset_ld, addcmd = '--unset=LD_LIBRARY_PATH '; end
fullcmd = sprintf('env %s CUDA_DEVICE_ORDER="PCI_BUS_ID" CUDA_VISIBLE_DEVICES=%s %s', ...
  addcmd, opts.gpu, cmd);
info.fullcmd = fullcmd;

actpath = pwd;
try
  cd(opts.runDir);
  if opts.verbose
    fprintf('Running:\n%s\n', fullcmd);
    tic;
    [ret, out] = system(fullcmd, '-echo');
    info.time = toc;
  else
    tic;
    [ret, out] = system(fullcmd);
    info.time = toc;
  end
catch e
  cd(actpath);
  throw(e);
end
cd(actpath);
if ret ~= 0
  error('Error running %s.\n%s', fullcmd, out);
end

end

