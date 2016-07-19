function [ d ] = framedist( fa, fb, ignoreOrientation )
if nargin < 3, ignoreOrientation = false; end;
assert(size(fa, 1) == size(fb, 1));
assert(size(fa, 2) == size(fb, 2));

useOrient = (size(fa, 1) == 3 || size(fa, 1) == 6) && ~ignoreOrientation;
if useOrient, fun = @dev; else fun = @noor_dev; end
fa = vl_frame2oell(fa);
fb = vl_frame2oell(fb);

d = zeros(1, size(fa, 2));
for fi = 1:size(fa, 2)
  d(fi) = fun(fa(:, fi), fb(:, fi));
end
end

function d = dev(fa, fb)
Aa = reshape(fa(3:6), 2, 2); Ta = fa(1:2);
Ab = reshape(fb(3:6), 2, 2); Tb = fb(1:2);

Af = Ab \ Aa - eye(2);
d = 0.25 * sum(diag(Af'*Af)) + sum((inv(Ab) * (Ta - Tb)).^2);
end

function d = noor_dev(fa, fb)
Aa = reshape(fa(3:6), 2, 2); Ta = fa(1:2);
Ab = reshape(fb(3:6), 2, 2); Tb = fb(1:2);

Af = Ab \ Aa;
s = sum(svd(Af));
d = 0.25 * (sum(diag(Af'*Af)) + 2 * (1 - s)) + sum((inv(Ab) * (Ta - Tb)).^2);
end
