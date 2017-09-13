% Setup and compile vlb, if run for the first time
run(fullfile(fileparts(mfilename('fullpath')), '..', 'matlab', 'vlb_setup.m'));
if ~exist(['vlb_greedy_matching.', mexext], 'file'), vlb_compile(); end;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Basic Commands

imdb = dset.vggh();
figure(1); clf;
vlb('view', 'matchpair', imdb, 1);

figure(2); clf;
vlb('view', 'matchpair', imdb, 1:5);

%% Run a detector and show detection
feat = vlb('detect', imdb, 'vlsift');
figure(3); clf;
vlb('view', 'detections', imdb, feat, 1);

%% Extract and visualise patches
vlb('extract', imdb, 'vlsift');
figure(3); clf;
vlb('view', 'patches', imdb, feat, 1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Repeatability example

feats = {};
feats{end+1} = vlb('detect', imdb, 'vlsift');
%MACOS doesn't support hesaff and haraff
if ~ismac
    feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'hesaff'});
    feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'haraff'});
end
res = cellfun(@(f) vlb('detrep', imdb, f), feats, 'Uni', false);
res = vertcat(res{:});

%% Display average repeatability per detector
display(varfun(@mean, res, 'InputVariables', 'repeatability',...
  'GroupingVariables', 'features'));

%% Plot the results

figure(10); clf;
subplot(1,2,1);
vlb('view', 'sequencescores', 'detrep', imdb, feats, 'graf', 'repeatability');
title('Graph Repetability');
subplot(1,2,2);
vlb('view', 'sequencescores', 'detrep', imdb, feats, 'graf', 'numCorresp');

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %% Matching score example

feats = {};
feats{end+1} = vlb('detect', imdb, 'vlsift');
%MACOS doesn't support hesaff and haraff
if ~ismac
    feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'hesaff'});
    feats{end} = vlb('describe', imdb, feats{end}, 'vggdesc');
    feats{end+1} = vlb('detect', imdb, 'vggaff', 'detArgs', {'detector', 'haraff'});
    feats{end} = vlb('describe', imdb, feats{end}, 'vggdesc');
end

res = cellfun(@(f) vlb('detmatch', imdb, f), feats, 'Uni', false);
res = vertcat(res{:});

%% Show the average matching score per detector
display(varfun(@mean, res, 'InputVariables', 'repeatability',...
  'GroupingVariables', 'features'));

%% Plot the results in a graph
figure(11); clf;
subplot(2,2,1);
vlb('view', 'sequencescores', 'detmatch', imdb, feats, 'graf', 'repeatability');
title('Graph Matching Score');
subplot(2,2,2);
vlb('view', 'sequencescores', 'detmatch', imdb, feats, 'graf', 'numCorresp');

%% View matched frames
%MACOS doesn't support hesaff and haraff
if ~ismac
    figure(21); clf;
    vlb('view', 'matches', imdb, feats{2}, 'detmatch', 3);
end
