run ./matlab/vlb_setup.m;
dbstop if error;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Repeatability example
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Single detector
imdb = dset.vggh();
% Compute repepatability for a single detector
vlb('detect', imdb, 'vlsift')
res = vlb('detrep', imdb, 'vlsift');

%% Set of detectors
feats = {};
feats{end+1} = vlb('detect', imdb, 'vlsift');
feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'hesaff'});
feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'haraff'});

res = cellfun(@(f) vlb('detrep', imdb, f), feats, 'Uni', false);
res = vertcat(res{:});

%% Display overall performance

display(varfun(@mean, res, 'InputVariables', 'repeatability',...
  'GroupingVariables', 'features'));

display(varfun(@mean, res, 'InputVariables', 'repeatability',...
  'GroupingVariables', {'features', 'sequence'}));

%% Plot the results

res_f = res(ismember(res.sequence, 'graf'), :);

figure(1); clf;
subplot(1,2,1);
for fi = 1:numel(feats)
  plot(res_f{ismember(res_f.features, feats{fi}), 'repeatability'});
  hold on;
end;
xlabel('Image'); ylabel('Repeatability'); grid on;
subplot(1,2,2);
for fi = 1:numel(feats)
  plot(res_f{ismember(res_f.features, feats{fi}), 'numCorresp'});
  hold on;
end;
xlabel('Image'); ylabel('Num Corresps.'); grid on;
legend(feats);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Matching score example
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

feats = {};
feats{end+1} = vlb('detect', imdb, 'vlsift');
feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'hesaff'});
feats{end} = vlb('describe', imdb, feats{end}, 'vggdesc');
feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'haraff'});
feats{end} = vlb('describe', imdb, feats{end}, 'vggdesc');

res = cellfun(@(f) vlb('detmatch', imdb, f), feats, 'Uni', false);
res = vertcat(res{:});

%%
display(varfun(@mean, res, 'InputVariables', 'repeatability',...
  'GroupingVariables', 'features'));

%% View matched frames
figure(1); clf;
vlb('view', 'matches', imdb, feats{2}, 'detmatch', 3);
