run ./matlab/vlb_setup.m;
dbstop if error;

%%

imdb = dset.vggh();

feats = {};
feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'hesaff'});
feats{end} = vlb('describe', imdb, feats{end}, 'vggdesc');
feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'hesaff'});
feats{end} = vlb('describe', imdb, feats{end}, 'vggdesc', 'descArgs', {'descriptor', 'gloh'});

res = cellfun(@(f) vlb('descmatch', imdb, f), feats, 'Uni', false);
res = vertcat(res{:});

%%

display(varfun(@mean, res, 'InputVariables', 'repeatability',...
  'GroupingVariables', 'features'));

display(varfun(@mean, res, 'InputVariables', 'repeatability',...
  'GroupingVariables', {'features', 'sequence'}));