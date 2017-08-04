function [x, info] = rootsift( patches )
% Copyright: Karel Lenc and Giorgos Tolias
info = struct('name', mfilename, 'describes', 'patches');

x = features.desc.sift(patches);
vnr = sum(abs(x));
x = bsxfun (@rdivide, x, vnr);
x = sqrt(x);
x(isnan(x)) = 0;
end

