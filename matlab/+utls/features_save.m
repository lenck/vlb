function features_save( path, features, varargin )
%FEATURES_SAVE Save a features structure at the specified path
opts.skipFields = {};
opts = vl_argparse(opts, varargin);

fields = setdiff(fieldnames(features), opts.skipFields);
[respath, imname] = fileparts(path);

for fi = 1:numel(fields)
  field = fields{fi};
  tgtpath = fullfile(respath, [imname, '.', field]);
  data = features.(field);
  switch class(data)
    case {'double', 'single', 'uint8'}
      dlmwrite([tgtpath, '.csv'], data', ';');
    case {'char'}
      fd = fopen([tgtpath, '.txt'], 'w');
      fprintf(fd, '%s', data);
      fclose(fd);
    otherwise
      save([tgtpath, '.mat'], '-v7.3', 'data');
  end
end

end

