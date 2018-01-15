function [ tf, info ] = randomtf( varargin )
opts.maxTr = 0;
opts.maxAffScRot = 0;
opts.maxRot = 0;
opts.maxScale = 0;
opts.minScale = 0;
opts.maxAnisotropy = 0;
opts.anisotropyShift = 0;
opts.q = RandStream('mt19937ar','Seed', 0);
opts.randfun = @(varargin) 2*rand(varargin{:}) - 1;
opts = vl_argparse(opts, varargin);

q = opts.q;

tha = opts.randfun(q, 1) * opts.maxAffScRot;
rota = [cos(tha) -sin(tha) ; sin(tha) cos(tha)];

% By default, the second rotation removes the affRotation
thb = opts.randfun(q, 1) * opts.maxRot - tha;
rotb = [cos(thb) -sin(thb) ; sin(thb) cos(thb)];

sc = 2.^(opts.randfun(q, 1) * (opts.maxScale - opts.minScale) + opts.minScale);
anis = 2.^(opts.randfun(q, 1) * opts.maxAnisotropy + opts.anisotropyShift);
scg = [sc / sqrt(anis) 0; 0 sc * sqrt(anis)];

Tg = opts.randfun(q, 2,1) * opts.maxTr ;
tf = [rotb*scg*rota, Tg; 0 0 1] ;

if nargout == 2
  info = struct('affScRot', tha, 'rot', thb, 'sc', sc, 'anis', anis);
end

end