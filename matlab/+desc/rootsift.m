function x = rootsift( patches )
% Copyright: Karel Lenc and Giorgos Tolias
x = desc.feats.patch_sift(patches);
vnr = sum(abs(x));
x = bsxfun (@rdivide, x, vnr);
x = sqrt(x);
x(isnan(x)) = 0;
end

