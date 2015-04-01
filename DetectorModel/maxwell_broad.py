import numpy as np

k_boltz = 1.38 #(g A^2)/(K s^2)
c = 3.0e18 #A/s
m_proton = 1.67e-24 #g

def maxwell_doppler_broadening(x,T,lambda0):
	sigma = np.sqrt((m_proton*lambda0)/(k_boltz*T))
	x = ((1./x)-(1./lambda0))**2.0
	amplitude = 1./np.sqrt(2.*np.pi*sigma)
	exponent = (-0.5*c**2.0*sigma**2.0)*x
	return amplitude*np.exp(exponent)

def produce_image(emisfile,tempfile,lambda.lfirst,lend,lstep):
	emisfrb = cPickle.load(open(emisfile,'rb'))
	tempfrb = cPickle.load(open(tempfile,'rb'))

	#wavelengths = np.linspace(lfirst,lend,Nstep,endpoint=True))
	wavelengths = np.arange(lfirst,lend,lstep)

	##I don't know if the 2d array of arrays will be the same as a 3d array.
	##must be possible to reshape it though....
	##let's see...

	return