function features_not_found( path )

variants = dir([path, '*']);
variants = variants([variants.isdir]);
variants = {variants.name};
if ~isempty(variants)
  error('Cannot find features in %s. \nDid you mean:\n%s', path, ...
    sprintf('\t%s\n', variants{:}));
else
  error('Cannot find features in %s.', path);
end

end

