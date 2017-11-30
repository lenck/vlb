function tf = frame2afftf( frame )
tf = zeros(3, 3, size(frame, 2));
if size(frame, 1) ~= 6
  frame = vl_frame2oell(frame);
end
tf(3, 3, :) = 1;
tf(1:2, 3, :) = frame(1:2, :);
tf(1:2, 1, :) = frame(3:4, :);
tf(1:2, 2, :) = frame(5:6, :);
end
