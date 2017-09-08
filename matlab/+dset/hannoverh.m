function imdb = hannoverh(varargin)
% HANNOVERH Wrapper around the Hannover Affine dataset

%
%   http://www.tnt.uni-hannover.de/project/feature_evaluation/
%
%   This class perform automatic installation when the dataset data
%   are not available.
%
%   Following options are supported:
%
%   Category :: ['graf']
%     The category within the VGG dataset, has to be one of
%     'graf','bark','bikes','grace','underground','colors','posters','there'
%
% References:
%   [1] Kai Cordes, Bodo Rosenhahn, Jörn Ostermann Increasing the 
%       Accuracy of Feature Evaluation Benchmarks Using Differential 
%       Evolution, IEEE Symposium Series on Computational Intelligence,
%       2011


opts.rootDir = fullfile(vlb_path(), 'data', 'dataset-hannover');
opts.matchFramesFun = @(g) ...
  @(fa, fb, varargin) geom.ellipse_overlap_H(g, fa, fb, ...
  'maxOverlapError', 0.5, varargin{:});
opts = vl_argparse(opts, varargin);

vggRootUrl = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/';
getVggDsetUrl = @(dset) [vggRootUrl, dset, '.tar.gz'];

% Meta about all datasets
sequences = {};
sequences{end+1} = struct('name', 'graf', 'description', 'Viewpoint angle', ...
  'labels', {{0 20 30 40 50 60}}, 'imext', 'ppm', 'packname', 'GrafHomAcc', 'addurl', '');
sequences{end+1} = struct('name', 'bark', 'description', 'Scale changes', ...
  'labels', {{1 1.2 1.8 2.5 3 4}}, 'imext', 'ppm', 'packname', 'BarkHomAcc', ...
  'addurl', getVggDsetUrl('bark'));
sequences{end+1} = struct('name', 'bikes', 'description', 'Increasing blur', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm', 'packname', 'BikesHomAcc', ...
  'addurl', getVggDsetUrl('bikes'));
sequences{end+1} = struct('name', 'grace', 'description', 'Viewpoint change', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm', 'packname', 'grace', 'addurl', '');
sequences{end+1} = struct('name', 'underground', 'description', 'Viewpoint change + patt. rep.', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm', 'packname', 'underground', 'addurl', '');
sequences{end+1} = struct('name', 'colors', 'description', 'Viewpoint change + patt. rep.', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm', 'packname', 'colors', 'addurl', '');
sequences{end+1} = struct('name', 'posters', 'description', 'Viewpoint change + text. rep.', ...
  'labels',  {{1 2 3 4 5 6}}, 'imext', 'ppm', 'packname', 'posters', 'addurl', '');
sequences{end+1} = struct('name', 'there','description', 'Viewpoint change', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm', 'packname', 'there', 'addurl', '');
sequences = cell2mat(sequences);
% Root url for dataset tarballs
rootUrl = 'http://www.tnt.uni-hannover.de/project/feature_evaluation/';
getDsetUrl = @(dset) [rootUrl, dset.name, sprintf('/%s.tar.gz', dset.packname)];
getImPath = @(dset, imid) fullfile(opts.rootDir, dset.name, ...
  sprintf('img%d.%s', imid, dset.imext));

% Download the datasets
for catIdx = 1:numel(sequences)
  dset = sequences(catIdx);
  dsetDir = fileparts(getImPath(dset, 1));
  utls.provision(getDsetUrl(dset), dsetDir);
  if ~isempty(dset.addurl)
    utls.provision(dset.addurl, dsetDir, 'doneName','.addurl.done');
  end
end

numImages = 6*numel(sequences);
imdb.images = cell(1, numImages);
imdb.tasks = {};

% Read the image information
imi = 1;
for catIdx = 1:numel(sequences)
  dset = sequences(catIdx);
  refim = imi;
  dsetDir = fileparts(getImPath(dset, 1));
  for imi_l = 1:6
    imPath = getImPath(dset, imi_l);
    assert(exist(imPath, 'file') == 2, 'Image %s not found.', imPath);
    imdb.images{imi}.id = imi;
    imdb.images{imi}.name = sprintf('%s-%d', dset.name, imi_l);
    imdb.images{imi}.path = imPath;
    imdb.images{imi}.seqnum = imi_l;
    imdb.images{imi}.sequence = dset.name;
    if imi_l == 1, imi = imi + 1; continue; end;
    imSize =  utls.get_image_size(imPath);
    tfs = utls.read_vgg_homography(fullfile(dsetDir, sprintf('H1to%dp', imi_l)));
    imdb.tasks{end+1} = struct('ima', imdb.images{refim}.name, ...
      'imb', imdb.images{imi}.name, 'H', tfs, ...
      'ima_size', imSize, 'imb_size', imSize, 'sequence', dset.name, ...
      'description', struct('impair', [1, imi_l], ...
      'nuisanceName', dset.description, 'nuisanceValue', dset.labels{imi_l}));
    imi = imi + 1;
  end
end
imdb.images = cell2mat(imdb.images);
imdb.tasks = cell2mat(imdb.tasks);
imdb.name = 'hannoverh';
imdb.matchFramesFun = opts.matchFramesFun;
imdb.geometry = 'homography';
imdb.rootdir = opts.rootDir;

end
