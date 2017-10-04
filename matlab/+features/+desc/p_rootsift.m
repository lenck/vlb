function [res] = p_rootsift( patches )
% Copyright: Karel Lenc and Giorgos Tolias
res = struct('descName', mfilename, 'describes', 'patches');

x = features.desc.p_sift(patches);
x = x.descs;
vnr = sum(abs(x));
x = bsxfun (@rdivide, x, vnr);
x = sqrt(x);
x(isnan(x)) = 0;
res.descs = x;
end

