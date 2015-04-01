wavelengths = np.arange(0.204-0.0012,0.204+0.0012+3.4e-6,3.4e-6)

wavelengths = np.arange(655.,661.1,0.1)[:-1]


step_function = np.zeros(len(wavelengths))
center = (len(wavelengths)-1.)/2.
step_function[center-2:center+3] = 1.0/(5.*0.034)


frb = np.zeros((len(wavelengths),100,100))
frb[:,45:55,45:55] = 30.

ip = ImageProducer(frb,658.,3.,0.1,2,0.,0.)

img = np.zeros((len(wavelengths),len(frb[0,:]),len(frb[1,:])))
gauss = Gaussian1DKernel(stddev=stddev)
zconvolve = convolve(step_function,gauss.array,boundary='extend')


for i in range(len(frb[0,:])):
   for j in range(len(frb[1,:])):
      img[:,i,j] = zconvolve*frb[:,i,j]


l = 328
end = 378

while l <= 378:
	I1 = integrate.simps(img[:,l,l], x)
	print I1
	i = i + 1
