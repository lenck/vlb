function [ img ] = covdet_preprocessim( img )
%COVDET_PREPROCESSIM Summary of this function goes here
%   Detailed explanation goes here
if isa(img, 'uint8'), img = im2single(img); end;
if isa(img, 'double'), img = single(img); end;
if size(img, 3) == 3, img = rgb2gray(img); end;

end

