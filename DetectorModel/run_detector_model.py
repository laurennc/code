from DetectorModel import *

lambda_center,lambda_range,lambda_res = 0.204,0.0012,3.4e-6
##UPADATE
eff_file = '??/FiltersDetector_V1/FIREBall_team_package/5LayerE_MeasRefl-Apr2014.txt' #choice arbitrary

##
testimage = 'FITS FILE HERE'

outputfile= 'detector_test'

#These are the values from Caltech but I initially tested with something larger
dc_val = 0.167
cic_val = 0.001 #0.0316

dm = DetectorModel(testimage, lambda_center, lambda_range, lambda_res, u.micron)

dm.build_efficiencyCube(eff_file)
dm.build_darkCurrentCube(dc_val)
dm.build_cicCube(cic_val)

dm.multiply_efficiency()
dm.add_detector_bkgd()

dm.sample_poisson()

##This makes a large number of plots
dm.plot_sample(outputfile)


