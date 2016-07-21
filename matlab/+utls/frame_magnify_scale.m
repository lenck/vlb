function [ frames ] = frame_magnify_scale( frames, mf )

if mf ~= 1
  frames = utls.frame_set_scale(frames, utls.frame_get_scale(frames) * mf);
end

end

