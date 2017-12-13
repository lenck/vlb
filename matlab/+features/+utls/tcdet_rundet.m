function [frames, score] = tcdet_rundet(imagepath, featspath, point_number, thr)

% Source: https://github.com/ColumbiaDVMM/Transform_Covariant_Detector/blob/master/tensorflow/point_extractor.m
% Author: Xu Zhang
% Adjusted for a single image calls: Karel Lenc

if ~exist('point_number', 'var'), point_number = 1000; end
if ~exist('thr', 'var'), thr = 1000; end

maxsize = 1024*768;
%Change this to your own vlfeat folder

%change point number to fix multiscale.
point_number = point_number/2;
pyramid_level = 5;
real_scale = 10;

feature = [];
score = [];
if ischar(imagepath)
  assert(exist(imagepath, 'file') == 2, 'Image not found');
  image = imread(imagepath);
else
  image = imagepath;
end
assert(exist(featspath, 'file') == 2, 'Features not found');
output = load(featspath);
output = output.output_list;
if numel(output)==0, error('Invalid features file.'); end

scale = 1.0;
if size(image,1)*size(image,2)>maxsize
  scale = sqrt(maxsize/(size(image,1)*size(image,2)));
  image = imresize(image,scale);
end

if size(image,3) > 3, image = image(:,:,1:3); end
if size(image,3)==1, image = repmat(image,1,1,3); end

for j = 1:numel(output)
  output{j} = permute(output{j},[3,1,2]);
end

for p = 1:pyramid_level
  if size(output{p},1)==0
    break
  end
  output_t = output{p};
  output{p} = zeros(6,size(output{p},2),size(output{p},3));
  output{p}(1,:,:) = 1;
  output{p}(5,:,:) = 1;
  if size(output_t,1)==6
    output{p}(3,:,:) = output_t(3,:,:);
    output{p}(6,:,:) = output_t(6,:,:);
  else
    output{p}(3,:,:) = output_t(1,:,:);
    output{p}(6,:,:) = output_t(2,:,:);
  end
  
  radius_factor = sqrt(2)^(p-1);
  
  outputs = permute(output{p},[2,3,1]);
  outputs(:,:,3) = outputs(:,:,3)*16*2/3;
  outputs(:,:,6) = outputs(:,:,6)*16*2/3;
  offset_x = (size(image,2)/radius_factor-size(outputs,2)*4)/2;
  offset_y = (size(image,1)/radius_factor-size(outputs,1)*4)/2;
  
  output_width = size(outputs,2);
  output_height = size(outputs,1);
  
  grid_x = (1:output_width)';
  grid_x = repmat(grid_x,1,output_height)*4+offset_x;
  grid_x = grid_x';
  
  grid_y = (1:output_height)';
  grid_y = repmat(grid_y,1,output_width)*4+offset_y;
  grid_x = grid_x - outputs(:,:,3);
  grid_y = grid_y - outputs(:,:,6);
  
  vote = zeros(size(grid_x));
  for j = 1:size(grid_x,1)
    for k = 1:size(grid_x,2)
      index_x = k-ceil(outputs(j,k,3)/4);
      index_y = j-ceil(outputs(j,k,6)/4);
      frac_x = ceil(outputs(j,k,3)/4) - outputs(j,k,3)/4;
      frac_y = ceil(outputs(j,k,6)/4) - outputs(j,k,6)/4;
      if (index_x)>=1&&(index_x+1)<=output_width&&(index_y)>=1&&(index_y+1)<=output_height
        vote(index_y+1,index_x+1) = vote(index_y+1,index_x+1)+frac_x*frac_y;
        vote(index_y+1,index_x) = vote(index_y+1,index_x)+frac_y*(1-frac_x);
        vote(index_y,index_x+1) = vote(index_y,index_x+1)+(1-frac_y)*frac_x;
        vote(index_y,index_x) = vote(index_y,index_x)+(1-frac_x)*(1-frac_y);
      end
    end
  end
  [vote, binary_img] = ApplyNonMax2Score(vote);
  binary_img = binary_img.*(vote>thr);
  
  vote = reshape(vote,1,output_width*output_height);
  grid_x = reshape(grid_x,1,output_width*output_height);
  grid_y = reshape(grid_y,1,output_width*output_height);
  real_output = reshape(outputs,output_width*output_height,6);
  binary_img = reshape(binary_img,1,output_width*output_height);
  
  vote(~binary_img) = [];
  grid_x(~binary_img) = [];
  grid_y(~binary_img) = [];
  real_output(~binary_img,:) = [];
  
  [~,idx] = sort(vote,'descend');
  
  grid_x = grid_x(idx(1:min(size(idx,2),round(point_number/radius_factor^2))));
  grid_y = grid_y(idx(1:min(size(idx,2),round(point_number/radius_factor^2))));
  real_output = real_output(idx(1:min(size(idx,2),round(point_number/radius_factor^2))),:);
  score_t = vote(idx(1:min(size(idx,2),round(point_number/radius_factor^2))))';
  if(isempty(grid_x))
    continue;
  end
  
  grid_x = grid_x.*radius_factor;
  grid_y = grid_y.*radius_factor;
  real_output = real_output.*radius_factor;
  
  real_output(:,3) = grid_x;
  real_output(:,6) = grid_y;
  feature_t = real_output;
  feature_t(:,[1,2,4,5]) = feature_t(:,[1,2,4,5])*real_scale;
  if(isempty(feature))
    feature = feature_t;
    score = score_t;
  else
    feature = [feature;feature_t];
    score = [score;score_t];
  end
end
frames = [(feature(:, 3)-1)./scale + 1, ...
  (feature(:, 6) - 1)./scale + 1, ...
  feature(:, 1)./scale]';
score = score';
end
