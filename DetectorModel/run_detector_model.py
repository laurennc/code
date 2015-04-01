from DectectorModel import *

wavelengths = np.linspace(2000.,2010.,50.)
testimage = np.zeros((len(wavelengths),100,100))
testimage[:,45:55,45:55] = 30.

outputfile= 'detector_test'

#These are the values from Caltech but I initially tested with something larger
dc_val = 0.167
cic_val = 0.0316

dm = DetectorModel(testimage,wavelengths)

dm.build_efficiencyCube('eff_test.dat')
dm.build_darkCurrentCube(dc_val)
dm.build_cicCube(cic_val)

dm.multiply_efficiency()
dm.add_detector_bkgd()

dm.sample_poisson()

dm.plot_sampe(outputfile)
