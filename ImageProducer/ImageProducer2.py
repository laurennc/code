import numpy as np
import matplotlib.pyplot as plt
import cPickle
from astropy.convolution import convolve, convolve_fft
from astropy.convolution import Gaussian1DKernel

class ImageProducer(object):
	"""ImageProducer receives one of the frb image arrays that I've produced.
	   It then convolves the image with a Gaussian of determinable size in order
	   to build the wavelength dimension. It will also scale the image for the 
	   correct redshift of interest.

	   The wavelengts are given in microns as is required by the IMO. The output
	   is in ergs cm^-2 s^-1 sr^-1 A^-1 """

	def __init__(self, frbarray,lambda_center,lambda_range,lambda_res,step_width,z_image,z_observed):
		#self.frb = cPickle.load(open(frbarray,'rb'))
		self.frb = frbarray
		#The wavelengths are set for the initial conditions agreed upon for the IMO
		self.wavelengths = np.arange(lambda_center-lambda_range,lambda_center+lambda_range+lambda_res,lambda_res)[:-1]
		#self.wavelengths = np.arange(0.204-0.0012,0.204+0.0012+3.4e-6,3.4e-6)
		
		#build the step function that will lead to the convolver shape
		self.step_function = np.zeros(len(self.wavelengths))
		center = (len(self.wavelengths)-1.)/2.
		##are these the right units??
		self.step_function[center-step_width/2.:center+step_width/2.+1] = 1.0/(step_width*lambda_res)

		self.z_image = z_image
		self.z_observed = z_observed

		self.img = 0

		##CAN DECIDE LATER IF I'D LIKE IT TO GET THE CENTRAL WAVELENGTH FROM THE FILE NAME
		##OR IF IT'S AN INPUT I WOULD LIKE TO OFFER

	def convolve_image(self,stddev,scale=True):
		##CURRENTLY BUILDING IMAGE AS LAMBA,X,Y
		img = np.zeros((len(self.wavelengths),len(self.frb[0,:]),len(self.frb[1,:])))


		gauss = Gaussian1DKernel(stddev=stddev)
		zconvolve = convolve(self.step_function,gauss.array,boundary='extend')

		
		for i in range(len(self.frb[0,:])):
			for j in range(len(self.frb[1,:])):
				if scale:
					img[:,i,j] = zconvolve*(self.frb[:,i,j]/((1.+self.z_observed)**4.0))
				else:
					img[:,i,j] = zconvolve*self.frb[:,i,j]

		return img

	def save_as_fits(self,outputname):
		
		return

	
