function [ tfframes ] = warpframe( frames, tf, method )
% WARPFRAME Warp a local feature frame with a homogprahy
%   WF = WARPFRAME(F, H) Warps frames F by homography H to generate warped
%     frames WF.
%     In case of a full Homography, an affine transformation at the frame
%     location is estimated using the second order Taylor polynom.
%
%   The Taylor expansion code - copyright K. Mikolajczyk.
if nargin < 3
  method = 'pre';
end

assert(all(size(tf) == [3, 3]));
frames = vl_frame2oell(frames);
ftf = helpers.frame2tf(frames);
tfs = zeros(size(ftf), 'like', ftf);
tfs(3, 3, :) = 1;

linearize = tf(3, 3) ~= 1 || any(tf(3, 1:2) ~= 0);
for i = 1:size(frames, 2)
  H = tf;
  if linearize % Linearise the affine transformation at feature point
    x = ftf(1, 3, i); y = ftf(2, 3, i);
    % H linearisation, originally from K. Mikolajczyk
    h11=H(1); h12=H(4); h13=H(7);
    h21=H(2); h22=H(5); h23=H(8);
    h31=H(3); h32=H(6); h33=H(9);
    fxdx=h11/(h31*x+h32*y+h33)-(h11*x+h12*y+h13)*h31/(h31*x+h32*y+h33)^2;
    fxdy=h12/(h31*x+h32*y+h33)-(h11*x+h12*y+h13)*h32/(h31*x+h32*y+h33)^2;
    fydx=h21/(h31*x+h32*y+h33)-(h21*x+h22*y+h23)*h31/(h31*x+h32*y+h33)^2;
    fydy=h22/(h31*x+h32*y+h33)-(h21*x+h22*y+h23)*h32/(h31*x+h32*y+h33)^2;
    Aff=[fxdx fxdy;fydx fydy];
    switch method
      case 'pre'
        C=H*[x;y;1]; C=C./C(3);
        tfs(1:2, 1:2, i) = Aff * ftf(1:2,1:2,i);
      case 'post'
        C=H*[0;0;1]; C=C./C(3);
        tfs(1:2, 1:2, i) = ftf(1:2,1:2,i) * Aff;
    end
    tfs(1:2, 3, i) = C(1:2);
  else
    switch method
      case 'pre'
        tfs(:,:, i) = H * ftf(:,:,i);
      case 'post'
        tfs(:,:, i) = ftf(:,:,i) * H;
    end
  end
end
tfframes = helpers.tf2frame(tfs);

end

