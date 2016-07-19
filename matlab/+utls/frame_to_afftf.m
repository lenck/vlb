function tf = frame_to_afftf( frame )
tf = zeros(3, 3, size(frame, 2));
tf(3, 3, :) = 1;
tf(1:2, 3, :) = frame(1:2, :);
tf(1:2, 1, :) = frame(3:4, :);
tf(1:2, 2, :) = frame(5:6, :);
end
