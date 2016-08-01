function [ ths ] = frame_get_orientation( frms )

frms = vl_frame2oell(frms);
ths = atan2(-frms(5, :), frms(6, :));

end
