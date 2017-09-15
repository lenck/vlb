function vlb_imagelist(imdb, feats, varargin)
%VLB_IMAGELIST Export imagelist and target paths to a txt file
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