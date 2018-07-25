function imid_out = getimid(imdb, imid)
if ischar(imid)
  [imid_out, status] = str2num(imid);
  if ~status
    imnames = {imdb.images.name};
    imname = imid;
    [found, imid_out] = ismember(imname, imnames);
    if ~found, error('Image %s not found.', imname); end
  end
else
  imid_out = imid;
end
if imid_out > numel(imdb.images) || imid_out < 1
  error('Invalid image id %d.', imid_out);
end
end