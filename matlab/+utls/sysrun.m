function [ out ] = sysrun( cmd, varargin )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
opts.gpu = [];
[opts, varargin] = vl_argparse(opts, varargin);
opts.unset_ld = isempty(opts.gpu); % Set true if segfaults, has to be false for CUDA
opts.runDir = pwd();
opts.verbose = false;
opts.env = struct();
opts = vl_argparse(opts, varargin);

if ~isempty(opts.gpu)
  opts.gpu = arrayfun(@num2str, opts.gpu - 1, 'Uni', false);
  opts.gpu = strjoin(opts.gpu, ',');
end

env.CUDA_DEVICE_ORDER = 'PCI_BUS_ID';
env.CUDA_VISIBLE_DEVICES = opts.gpu;
env = vl_override(env, opts.env);
envstr = envstring(env);

addcmd = '';
if opts.unset_ld, addcmd = '--unset=LD_LIBRARY_PATH '; end
fullcmd = sprintf('env %s %s %s', addcmd, envstr, cmd);

actpath = pwd;
try
  cd(opts.runDir);
  if opts.verbose
    fprintf('Running:\n%s\n', fullcmd);
    [ret, out] = system(fullcmd, '-echo');
  else
    [ret, out] = system(fullcmd);
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

function str = envstring(env)
flds = fieldnames(env);
str = '';
for fi = 1:numel(flds)
  str = [str flds{fi}, '=', env.(flds{fi}), ' '];
end
end
