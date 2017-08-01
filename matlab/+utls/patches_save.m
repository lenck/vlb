function patches_save(patches, respath)
assert(size(patches, 3) == 1 || size(patches, 3) == 3, ...
  'Patches has to be stored along 4th dimension.');
patchim = vl_imarray(squeeze(patches), 'Layout', [size(patches, 4), 1]);
imwrite(patchim, respath);
end