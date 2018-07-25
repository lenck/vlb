function helpbuilder(cmds, cmd, varargin)
opts.name = 'vlb';
opts = vl_argparse(opts, varargin);
fname = opts.name;
if isdeployed(), opts.name = sprintf('run_%s.sh', opts.name); end;
if isempty(cmd) || strcmp(cmd, 'help')
  fprintf('Usage: `%s COMMAND ...\n', opts.name);
  printhelp(fname);
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
      func = func2str(cmds.(cmd).fun);
      printhelp(func);
    else
      cmds.(cmd).help(cmd);
    end
  else
    error('Invalid command. Run %s help for list of valid commands', opts.name);
  end
end
end

function printhelp(func)
if isdeployed
  parsehelp(func);
else
  help(func);
end
end

function parsehelp(fun)
fun_path = fullfile(de_path(), [fun, '.m']);
fun_src = fileread(fun_path);
help_end = strfind(fun_src, '% Copyright') - 1;
fun_src = fun_src(1:help_end);
fun_src = splitlines(fun_src);
fun_src = cellfun(@(a) a(2:end), fun_src(2:end), 'Uni', false);
help_str = strjoin(fun_src, newline);
fprintf(help_str);
end