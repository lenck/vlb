function [wfrm, refb, refa] = warpim_H(ima, H, varargin)
opts.warp_method = 'imwarp';
opts.invert = false;
opts = vl_argparse(opts, varargin);

refa = zb_imref(size(ima));
switch opts.warp_method
  case 'interp'
    refb = zb_imref(size(ima));
    [R_n, C_n] = ndgrid(1:size(ima, 1), 1:size(ima, 2));
    P_n = [C_n(:), R_n(:)]';
    if opts.invert
      P_i = p2e(H\e2p(P_n));
    else
      P_i = p2e(H*e2p(P_n));
    end
    
    % 'Query' rows and columns
    R_i = reshape(P_i(2,:), size(ima, 1), size(ima, 2));
    C_i = reshape(P_i(1,:), size(ima, 1), size(ima, 2));
    
    wfrm = cell(1, 1, size(ima, 3));
    for ci = 1:size(ima, 3)
      wfrm{ci} = interp2(double(ima(:,:,ci)), C_i, R_i);
    end
    wfrm = uint8(cell2mat(wfrm));
  case 'imwarp'
    tf = projective2d(H');
    if ~opts.invert
      tf = tf.invert();
    end
    [wfrm, refb] = imwarp(ima, refa, tf);
  otherwise
    error('Unsupported warp method %s.', opts.warp_method);
end
end

function [ ra ] = zb_imref( imsz )
%Get an image reference frame for zero based coordinates.

ra = imref2d([imsz(1), imsz(2)], [-0.5, imsz(2)-0.5], ...
  [-0.5, imsz(1)-0.5]);
end

function [ pts ] = e2p( pts )
pts = [pts;ones(1,size(pts,2))];
end

function [ pts ] = p2e( pts )
pts = pts./repmat(pts(size(pts,1),:),size(pts,1),1);
pts = pts(1:size(pts,1)-1,:);
end
