import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy import interpolate
from astropy import units as u

class DetectorModel(object):
	"""DetectorModel receives an image array from the Instrument Model and then adds
	    the relevant noise and efficiencies. Poisson realizations from these expected
	    values can be created and plotted. """

	#The cubes are set up such that lambda is the first axis
	#The wavelength range should be within the efficiency file for the interpolation to work

	def __init__(self, instrumentImage, lambda_center, lambda_range, lambda_res, wavelength_unit):
		#Input from the instrument model
		self.expectedValueImage = instrumentImage

		#Need to know wavelengths of the observations. x,y less important
		#self.wavelengths = wavelengths
		self.wavelength_unit = wavelength_unit

		lrange = math.ceil((2.*lambda_range)/lambda_res)/2.
		self.wavelengths = np.arange(-1.*lrange,lrange+1,1)*lambda_res+lambda_center

		#holders for cubes that will hold Parts of the Model 
		self.efficiencyCube = []
		self.cicCube = []
		self.darkCurrentCube = []

		#holders for the eventual Poisson realizations of the expected value image
		self.poissonRealizations = []
		self.currentRealization = []
		

	#This function should be able to read in filter efficiency, interpolate it, then produce 
	#cube at the wavelengths of interest
	def build_efficiencyCube(self,filein):
		######NEED TO MAKE SURE WAVELENGTH UNITS MATCH ##############
		data = np.genfromtxt(filein)
		lambda_unit = u.nanometer
		#write now really specialized for 2 column file
		eff_func = interpolate.interp1d(data[:,0],data[:,1],kind='cubic')
		xs = (self.wavelengths*self.wavelength_unit).to(u.nanometer)
		xs = xs.value
		eff_vals = eff_func(xs)

		self.efficiencyCube = np.zeros(self.expectedValueImage.shape)
		for i in range(len(self.wavelengths)):
			self.efficiencyCube[i,:,:] = eff_vals[i]
		return

	#Right now, don't really need since using a single value but easier to generalize
	#this way
	def build_darkCurrentCube(self,val):
		#I can't remember if this has a wavelength dependency or not....
		self.darkCurrentCube = np.zeros(self.expectedValueImage.shape) + val
		return

	#Right now, don't really need since using a single value but easier to generalize
	#this way
	def build_cicCube(self,val):
		self.cicCube = np.zeros(self.expectedValueImage.shape) + val
		return

	#These next two functions apply the generated cubes to the instrument model image
	def multiply_efficiency(self):
		self.expectedValueImage = self.expectedValueImage*self.efficiencyCube
		return

	def add_detector_bkgd(self,CIC=True,DarkCurrent=True):
		if CIC:
			self.expectedValueImage = self.expectedValueImage + self.cicCube
		if DarkCurrent:
			self.expectedValueImage = self.expectedValueImage + self.darkCurrentCube
		return

	#Make a Poisson realization of current expected value image
	#Note: This function will work with the provided instrument model without anything
	#else applied, or at each step in the processing. 
	def sample_poisson(self):
		self.currentRealization = np.random.poisson(lam=self.expectedValueImage)
		self.poissonRealizations = np.append(self.poissonRealizations,self.currentRealization)
		return

	#A simple function to make plots of the detector surface at each wavelength. Individual
	#plot generated for each wavelength bin
	def plot_sample(self,outputfile_base,idx=None):
		if idx==None:
			for i in range(len(self.wavelengths)):
				im = plt.imshow(self.currentRealization[i,:,:],interpolation=None)
				plt.colorbar(im)
				plt.savefig(outputfile_base+str(i)+'.png')
				plt.close()
		elif idx:
			for i in range(len(self.wavelengths)):
				im = plt.imshow(self.poissonRealizations[idx][i,:,:],interpolation=None)
				plt.colorbar(im)
				plt.savefig(outputfile_base+str(i)+'.png')
				plt.close()
		else:
			print 'This is either an invalid index or you have not sampled!'
		return