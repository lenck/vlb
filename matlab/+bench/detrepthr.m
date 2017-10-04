function [ res, info ] = detrepthr( matchFrames, featsa, featsb, varargin )
% VLB_THR_REPEATABILITY Compute a repetability over a set of thresholds
opts.normFactor = 'b';
opts = vl_argparse(opts, varargin);
fa = featsa.frames; fb = featsb.frames;
fsca = featsa.detresponses; fscb = featsb.detresponses;
  
res = struct('repeatability', [], 'numCorresp', [], 'numDets',[]);
info = struct('geomMatches', zeros(2, 0));
if isempty(fa) || isempty(fb), return; end
if ~iscell(fa), fa = {fa}; end; if ~iscell(fsca), fsca = {fsca}; end;
if ~iscell(fb), fb = {fb}; end; if ~iscell(fscb), fscb = {fscb}; end
if ~iscell(matchFrames), matchFrames = {matchFrames}; end;

if numel(fa) == 1 && numel(fb) > 1
  fa = repmat(fa, 1, numel(fb)); 
  fsca = repmat(fsca, 1, numel(fb));
end
assert(numel(matchFrames) == numel(fb));
assert(numel(fa) == numel(fb));
assert(numel(fsca) == numel(fb));
assert(numel(fscb) == numel(fb));

arr = cell(1, numel(fa)); info = cell(1, numel(fa));
for ci = 1:numel(fa)
  [tcorr, tcorr_score, info{ci}] = matchFrames{ci}(fa{ci}, fb{ci});
  info{ci}.tcorr = tcorr; info{ci}.corr_score = tcorr_score;
  fa_num = sum(info{ci}.fa_valid); 
  fb_num = sum(info{ci}.fb_valid);
  %if isempty(tcorr), return; end;
  fsca{ci} = fsca{ci}(:, info{ci}.fa_valid);
  fscb{ci} = fscb{ci}(:, info{ci}.fb_valid);
  tcorr_fsc = min([fsca{ci}(tcorr(1, :)); fscb{ci}(tcorr(2, :))], [], 1);
  
  % Sort the edgest by decrasing score
  [tcorr_fsc, perm] = sort(tcorr_fsc, 'descend');
  tcorr = tcorr(:, perm);
  % Approximate the best bipartite matching
  matches = vlb_greedy_matching(fa_num, fb_num, tcorr');
  info{ci}.geomMatches = matches;
  
  tcorr_matched = false(1, size(tcorr, 2));
  tcorr_matched(matches(2, matches(2, :)>0)) = true;
  %arr = [iscorrect, isdetection, score]
  % matches and detections put side by side to be able to compute the
  % number of detections per threshold
  arr{ci} = [tcorr_matched; zeros(1, numel(tcorr_matched)); tcorr_fsc];
  if strcmp(opts.normFactor, 'minab')
    if numel(fsca{ci}) > numel(fscb{ci})
      opts.normFactor = 'b';
    else
      opts.normFactor = 'a';
    end
  end
  switch opts.normFactor
    case 'a'
      arr{ci} = [arr{ci} [zeros(1, size(fsca{ci}, 2)); ones(1, size(fsca{ci}, 2)); fsca{ci}]];
    case 'b'
      arr{ci} = [arr{ci} [zeros(1, size(fscb{ci}, 2)); ones(1, size(fscb{ci}, 2)); fscb{ci}]];
  end
end

arr = cell2mat(arr); info = cell2mat(info);
[~, perm] = sort(arr(3, :), 'descend');
arr = arr(:, perm);
nmatches = cumsum(arr(1, :));
ndet = cumsum(arr(2, :)) + 1;
rep = nmatches ./ ndet;

res.repeatability = rep;
res.numMatches = nmatches;
res.numDets = ndet;