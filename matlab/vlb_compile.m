function vlb_compile(varargin)
%VLB_COMPILE Compile the VLB toolbox.
%   The `vlb_compile()` function compiles the MEX files in the
%   VLB toolbox.
%
%   `vlb_compile('OPTION', ARG, ...)` accepts the following options:
%
%   `Verbose`:: 0
%      Set the verbosity level (0, 1 or 2).
%
%   `Debug`:: `false`
%      Set to true to compile the binaries with debugging
%      information.
%
%   Generally, you only need a 64bit C/C++ compiler (usually Xcode, GCC or
%   Visual Studio for Mac, Linux, and Windows respectively). The
%   compiler can be setup in MATLAB using the
%
%      mex -setup
%
%   command.

% Copyright (C) 2014-16 Karel Lenc and Andrea Vedaldi.
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

% Get VLB root directory
root = fileparts(fileparts(mfilename('fullpath'))) ;
addpath(fullfile(root, 'matlab')) ;

% --------------------------------------------------------------------
%                                                        Parse options
% --------------------------------------------------------------------

opts.verbose = 0;
opts.debug   = false;
% Files to compile
opts.lib_src = {};
opts.mex_src = {...
  fullfile(root, 'matlab', 'src', 'vgg_compute_ellipse_overlap.cpp'), ...
  fullfile(root, 'matlab', 'src', 'vlb_greedy_matching.cpp')};
% Compiler flags
opts.cc = {} ;
opts.ccpass = {} ;
opts.ccoptim = {} ;
opts.link = {} ;
opts.linklibs = {} ;
opts.linkpass = {} ;
% Build directories
opts.mex_dir = fullfile(root, 'matlab', 'mex');
[opts, varargin] = vl_argparse(opts, varargin);
opts.bld_dir = fullfile(opts.mex_dir, '.build');
opts = vl_argparse(opts, varargin);

% --------------------------------------------------------------------
%                                                     Compiler options
% --------------------------------------------------------------------

if opts.verbose > 1
  opts.cc{end+1} = '-v' ;
end
if opts.debug
  opts.cc{end+1} = '-g' ;
else
  opts.cc{end+1} = '-DNDEBUG' ;
end

arch = computer();
switch arch
  case {'maci64'}
    opts.ccpass{end+1} = '-mmacosx-version-min=10.9' ;
    opts.linkpass{end+1} = '-mmacosx-version-min=10.9' ;
    opts.ccoptim{end+1} = '-mssse3 -ffast-math' ;
  case {'glnxa64'}
    opts.ccoptim{end+1} = '-mssse3 -ftree-vect-loop-version -ffast-math -funroll-all-loops' ;
end

% --------------------------------------------------------------------
%                                                        Command flags
% --------------------------------------------------------------------

opts.mexcc = horzcat(opts.cc, ...
                      {'-largeArrayDims'}, ...
                      {['CXXFLAGS=$CXXFLAGS ' strjoin(opts.ccpass)]}, ...
                      {['CXXOPTIMFLAGS=$CXXOPTIMFLAGS ' strjoin(opts.ccoptim)]}) ;
if ~ispc, opts.mexcc{end+1} = '-cxx'; end

% mex: link
opts.mexlink = horzcat(opts.cc, opts.link, ...
                        {'-largeArrayDims'}, ...
                        {['LDFLAGS=$LDFLAGS ', strjoin(opts.linkpass)]}, ...
                        {['LINKLIBS=$LINKLIBS ', strjoin(opts.linklibs)]}) ;

if opts.verbose
  fprintf('%s: * Compiler and linker configurations *\n', mfilename) ;
  fprintf('%s: \tintermediate build products directory: %s\n', mfilename, opts.bld_dir) ;
  fprintf('%s: \tMEX files: %s/\n', mfilename, opts.mex_dir) ;
  fprintf('%s: \tMEX options [CC CPU]: %s\n', mfilename, strjoin(opts.mexcc)) ;
  fprintf('%s: \tMEX options [LINK]: %s\n', mfilename, strjoin(opts.mexlink)) ;
end

% --------------------------------------------------------------------
%                                                              Compile
% --------------------------------------------------------------------

% Intermediate object files
srcs = horzcat(opts.lib_src, opts.mex_src) ;
for i = 1:numel(horzcat(opts.lib_src, opts.mex_src))
  [~, ~, ext] = fileparts(srcs{i}) ; ext(1) = [] ;
  objfile = toobj(opts, srcs{i});
  mex_compile(opts, srcs{i}, objfile) ;
  assert(exist(objfile, 'file') ~= 0, 'Compilation of %s failed.', objfile);
end

% Link into MEX files
for i = 1:numel(opts.mex_src)
  objs = toobj(opts, [opts.mex_src(i), opts.lib_src]) ;
  mex_link(opts, objs) ;
end

% Reset path adding the mex subdirectory just created
vlb_setup() ;

% --------------------------------------------------------------------
%                                                    Utility functions
% --------------------------------------------------------------------

% --------------------------------------------------------------------
function objs = toobj(opts ,srcs)
% --------------------------------------------------------------------
str = fullfile('matlab','src') ;
multiple = iscell(srcs) ;
if ~multiple, srcs = {srcs} ; end
objs = cell(1, numel(srcs));
for t = 1:numel(srcs)
  i = strfind(srcs{t},str);
  objs{t} = fullfile(opts.bld_dir, srcs{t}(i+numel(str):end)) ;
end
if ~multiple, objs = objs{1} ; end
objs = regexprep(objs,'.cpp$',['.' objext]) ;
objs = regexprep(objs,'.c$',['.' objext]) ;

% --------------------------------------------------------------------
function mex_compile(opts, src, tgt)
% --------------------------------------------------------------------
mopts = {'-outdir', fileparts(tgt), src, '-c', opts.mexcc{:}} ;
opts.verbose && fprintf('%s: MEX CC: %s\n', mfilename, strjoin(mopts)) ;
mex(mopts{:}) ;

% --------------------------------------------------------------------
function mex_link(opts, objs)
% --------------------------------------------------------------------
mopts = {'-outdir', opts.mex_dir, opts.mexlink{:}, objs{:}} ;
opts.verbose && fprintf('%s: MEX LINK: %s\n', mfilename, strjoin(mopts)) ;
mex(mopts{:}) ;

% --------------------------------------------------------------------
function ext = objext()
% --------------------------------------------------------------------
% Get the extension for an 'object' file for the current computer
% architecture
switch computer('arch')
  case 'win64', ext = 'obj';
  case {'maci64', 'glnxa64'}, ext = 'o' ;
  otherwise, error('Unsupported architecture %s.', computer) ;
end

