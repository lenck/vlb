function [ anis ] = frame_get_anisotropy( frames )

tfs = utls.frame2afftf(vl_frame2oell(frames));
anis = zeros(1, size(frames, 2));
for fi = 1:size(frames, 2)
  s = svd(tfs(1:2,1:2,fi));
  anis(fi) = s(1) ./ s(2);
end

end

