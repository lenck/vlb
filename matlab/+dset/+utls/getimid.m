function imid = getimid(imdb, imid)
if ischar(imid)
  imnames = {imdb.images.name};
  imname = imid;
  [found, imid] = ismember(imname, imnames);
  if ~found, error('Image %s not found.', imname); end;
end
if imid > numel(imdb.images) || imid < 1
  error('Invalid image id %d.', imid);
end
end