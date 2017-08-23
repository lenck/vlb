function [ res ] = sift( patches )
res = struct('descName', mfilename, 'describes', 'patches', 'descs', []);
if isempty(patches), return; end;

psz = [size(patches, 1), size(patches, 2)];
frm = [(psz(1) ./ 2 + 0.5) * ones(2, 1) ; psz(1) ./ 2; 0];
x = [];
for pi = 1:size(patches, 4)
  I = single(patches(:, :, 1, pi));
  [Ix, Iy] = vl_grad(I) ;
  mod      = sqrt(Ix.^2 + Iy.^2) ;
  ang      = atan2(Iy, Ix) ;
  grd      = shiftdim(cat(3, mod, ang), 2) ;
  d        = vl_siftdescriptor(grd, frm, 'magnif', 0.5) ;
  if isempty(x)
    x = zeros(numel(d), size(patches, 4), 'single');
  end
  x(:, pi) = d;
end
res.descs = x;
end

