run ./matlab/vlb_setup.m;
dbstop if error;

%% Run the experiment
imdb = dset.vggh();

dets = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'hesaff'});

feats = {};
feats{end+1} = vlb('describe', imdb, dets, 'vggdesc');
feats{end+1} = vlb('describe', imdb, dets, 'vggdesc', ...
  'descArgs', {'descriptor', 'gloh'});

res = cellfun(@(f) vlb('descmatch', imdb, f), feats, 'Uni', false);
res = vertcat(res{:});

%% Show the mAP
display(varfun(@mean, res, 'InputVariables', 'ap',...
  'GroupingVariables', 'features'));

%% Plot the precision recall curves
figure(1); clf;
vlb('view', 'descmatchpr', imdb, feats, 2);
legend(feats, 'Location', 'SW');
