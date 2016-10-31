run ./matlab/vlb_setup.m;
dbstop if error;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Repeatability example
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dset = vlb_dataset_vggaffine('graf');

dog_det = @(im) vl_sift(single(im));
hesaff_det = @(im) legacy.vgg_aff(im, 'detector', 'hesaff');
dets = {dog_det, hesaff_det};

%% Compute the results

rep = zeros(numel(dets), 5); nm = rep;
images = arrayfun(@(imi) dset.getGsImage(imi), 1:6, 'Uni', false);
for di = 1:numel(dets)
  det = dets{di}; fa = det(images{1});
  for imi = 2:6
    match_geom = @(fa, fb) vlb_ellipse_overlap_H(dset.getGeom(imi), ...
      fa, fb, 'mode', 'detectors');
    [rep(di, imi-1), nm(di, imi-1)] = vlb_repeatability(...
      match_geom, fa, det(images{imi}));
    fprintf('.');
  end
  fprintf('\n');
end

%% Plot the results

figure(1); clf;
subplot(1,2,1); plot(2:6, rep);
xlabel('Image'); ylabel('Repeatability'); grid on;
subplot(1,2,2); plot(2:6, nm);
xlabel('Image'); ylabel('Num Matches'); grid on;
legend('DoG', 'HesAff');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Matching score example
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dset = vlb_dataset_vggaffine('graf');

dog_det = @(im) vl_sift(single(im));
hesaff_det = @(im) legacy.vgg_aff(im, 'detector', 'hesaff');
dets = {dog_det, hesaff_det};

sift_desc = @(im, det) legacy.vgg_desc(im, det(im), 'descriptor', 'sift');


%% Compute the results
ms = zeros(numel(dets), 5); nm = rep;
images = arrayfun(@(imi) dset.getGsImage(imi), 1:6, 'Uni', false);
for di = 1:numel(dets)
  det = dets{di};
  [fa, da] = desc(images{1}, det);
  for imi = 2:6
    [fb, db] = desc(images{imi}, det);
    match_geom = @(fa, fb) vlb_ellipse_overlap_H(dset.getGeom(imi), ...
      fa, fb, 'mode', 'descriptors');
    [ms(di, imi-1), nm(di, imi-1)] = vlb_matchingscore(...
      match_geom, fa, da, fb, db);
    fprintf(':');
  end
  fprintf('\n');
end

%% Plot the results
figure(1); clf;
subplot(1,2,1); plot(2:6, ms);
xlabel('Image'); ylabel('Repeatability'); grid on;
subplot(1,2,2); plot(2:6, nm);
xlabel('Image'); ylabel('Num Matches'); grid on;
legend('DoG', 'HesAff');