function helpbuilder(cmds, cmd, varargin)
opts.name = 'vlb';
opts = vl_argparse(opts, varargin);
if isdeployed(), opts.name = sprintf('run_%s.sh', opts.name); end;
if isempty(cmd) || strcmp(cmd, 'help')
  fprintf('Usage: `%s COMMAND ...\n', opts.name);
  help(opts.name);
  if usejava('desktop')
    fprintf('Valid commands:\n\t');
    cmd_names = fieldnames(cmds);
    for ci = 1:(numel(cmd_names))
      fprintf('<a href="matlab: %s help %s">%s</a>  ', ...
        opts.name, cmd_names{ci}, cmd_names{ci});
    end
    fprintf('\n');
  else
    fprintf('Valid commands: %s\n\n', strjoin(fieldnames(cmds), ', '));
  end
else
  if isfield(cmds, cmd)
    fprintf('Help for %s command `%s`:\n', opts.name, cmd);
    if isempty(cmds.(cmd).help)
      help(func2str(cmds.(cmd).fun));
    else
      cmds.(cmd).help(cmd);
    end
  else
    error('Invalid command. Run %s help for list of valid commands', opts.name);
  end
end
end