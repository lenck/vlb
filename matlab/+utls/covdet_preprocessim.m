function [ img ] = covdet_preprocessim( img )
%COVDET_PREPROCESSIM Preprocess image for the VL_COVDET function
%   Prepares the image to single and in the [0, 1], single channel
%   range, which is expected by VL_COVDET and VL_SIFT (e.g. all 
%   thresholds are set for these ranges).
%
%  See also: vl_covdet, vl_sift
if isa(img, 'uint8'), img = im2single(img); end;
if isa(img, 'double'), img = single(img); end;
if size(img, 3) == 3, img = rgb2gray(img); end;

end

