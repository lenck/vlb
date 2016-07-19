run ./matlab/vlb_setup.m;
dbstop if error;

%%

dset = vlb_dataset_vggaffine('graf');
det = @(im) legacy.vgg_aff(im, 'detector', 'hesaff');
desc = @(im, det) legacy.vgg_desc(im, det(im), 'descriptor', 'sift');

imb_i = 4;
ima = dset.getGsImage(1); imb = dset.getGsImage(imb_i);
match_geom = @(fa, fb) vlb_ellipse_overlap_H(dset.getGeom(imb_i), fa, fb, ...
  'mode', 'descriptors');

%%
figure(1); clf;
subplot(1,2,1); imshow(ima); subplot(1,2,2); imshow(imb);

%%
fprintf('Computing features.\n');
[fa, da] = desc(ima, det); [fb, db] = desc(imb, det);

%%
figure(1); clf; fprintf('Matching...\n');

[prec, recall, info] = vlb_desc_benchmark(match_geom, fa, da, fb, db, ...
  'MatchingStrategy', 'threshold');
subplot(1,3,1); plot(1-prec, recall);
axis square; set(gca, 'ylim', [0, 1]); title('THR');
xlabel('1-precision'); ylabel(sprintf('#correct/%d', info.numCorresp));

[prec, recall, info] = vlb_desc_benchmark(match_geom, fa, da, fb, db, ...
  'MatchingStrategy', 'nn');
subplot(1,3,2); plot(1-prec, recall);
axis square; set(gca, 'ylim', [0, 1]);  title('NN');
xlabel('1-precision'); ylabel(sprintf('#correct/%d', info.numCorresp));

[prec, recall, info] = vlb_desc_benchmark(match_geom, fa, da, fb, db, ...
  'MatchingStrategy', 'nndistratio');
subplot(1,3,3); plot(1-prec, recall);
axis square; set(gca, 'ylim', [0, 1]); title('NN Dist Ratio');
xlabel('1-precision'); ylabel(sprintf('#correct/%d', info.numCorresp));

%%

[vgg_res, vgg_info] = legacy.vgg_desc_benchmark(dset.getGeom(imb_i), ...
  fullfile(dset.imageDir, dset.images.name{1}), fa, da, ...
  fullfile(dset.imageDir, dset.images.name{imb_i}), fb, db);

%%

figure(2); clf;
subplot(1,3,1);
plot(1 - vgg_res.threshold.precision, vgg_res.threshold.recall); 
axis square;  set(gca, 'ylim', [0, 1]); title('THR');
xlabel('1-precision'); ylabel(sprintf('#correct/%d', vgg_info.numSimCorresp));

subplot(1,3,2);
plot(1 - vgg_res.nn.precision, vgg_res.nn.recall); 
axis square;  set(gca, 'ylim', [0, 1]); title('NN');
xlabel('1-precision'); ylabel(sprintf('#correct/%d', vgg_info.numCorresp));

subplot(1,3,3);
plot(1 - vgg_res.nndistratio.precision, vgg_res.nndistratio.recall);
axis square;  set(gca, 'ylim', [0, 1]); title('NN Dist Ratio');
xlabel('1-precision'); ylabel(sprintf('#correct/%d', vgg_info.numCorresp));

