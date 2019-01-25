function [ res ] = filedet( img, varargin )

res.detName = sprintf('FILEDET');
if isempty(img), res.frames = zeros(4, 0); return; end

if ischar(img)
  imgname = img;
else
  imgname = 'binary data';
end
error('Features for an image do not exist (%s)', imgname);

end

