function [ im ] = imread_grayscale( varargin )
%IMREAD_GRAYSCALE Read an image to a grayscale
%   IMREAD_GRAYSCALE accepts the same arguments as imread. If an image is
%   in RGB, converts to grayscale image.

im = imread(varargin{:});
if size(im, 3) == 3, im = rgb2gray(im); end

