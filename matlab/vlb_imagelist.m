function vlb_imagelist(imdb, feats, varargin)
%VLB_IMAGELIST Export imagelist and target paths to a txt file
%  VLB_IMAGELIST imdb featsname

% Copyright (C) 2016-2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.targetDir = fullfile(vlb_path(), 'data');
opts = vl_argparse(opts, varargin);

imdb = dset.factory(imdb);
if isstruct(feats), feats = feats.name; end;
featsname = genvarname(feats);
tgt_path = fullfile(opts.targetDir, sprintf('%s-%s.csv', imdb.name, featsname));

out = fopen(tgt_path, 'w');
for imi = 1:numel(imdb.images)
  impath = imdb.images(imi).path;
  tgtpath = fullfile(vlb_path('features', imdb, feats), [imdb.images(imi).name]);
  fprintf(out, '%s;%s;%s\n', impath, [tgtpath '.frames.csv'], [tgtpath '.descs.csv']);
end
fclose(out);
fprintf('Output exported to %s\n', tgt_path);

end