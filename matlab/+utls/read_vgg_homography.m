function [ tfs ] = read_vgg_homography( path )
%UNTITLED7 Summary of this function goes here
%   Detailed explanation goes here
if ~exist(path, 'file')
  error('File %s does not exist.', path);
end
tfs = eye(3);
[tfs(:,1), tfs(:,2), tfs(:,3)] = textread(path, '%f %f %f%*[^\n]');

end

