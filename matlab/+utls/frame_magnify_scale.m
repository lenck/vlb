function [ frames ] = frame_magnify_scale( frames, mf )

frames = utls.frame_set_scale(frames, utls.frame_get_scale(frames) * mf);

end

