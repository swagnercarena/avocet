from AbundanceMatching import AbundanceFunction, calc_number_densities
import numpy as np
from Corrfunc.theory import wp

def generate_wp(lf,halos,af_criteria,r_p_data,box_size,mag_cut,pimax=40.0,
	nthreads=1):
	"""	Generate the projected 2D correlation by abundance matching galaxies
		Parameters:
			lf: The luminosity function. The first column is the magnitudes and the
				second column is the density in units of 1/Mpc^3.
			halos: A catalog of the halos in the n-body sim that can be indexed
				into using the quantity name.
			af_criteria: The galaxy property (i.e. vpeak) to use for abundance 
				matching.
			r_p_data: The positions at which to calculate the 2D correlation
				function.
			box_size: The size of the box (box length not volume)
			mag_cut: The magnitude cut for w_p(r_p)
			pimax: The maximum redshift seperation to use in w_p(r_p) calculation
			nthreads: The number of threads to use for CorrFunc
		Returns:
			w_p(r_p) at the r_p values specified by r_p_data.
	"""

	# Initialize abundance function and calculate the number density of the
	# halos in the box
	af = AbundanceFunction(lf[:,0], lf[:,1], (-25, -5))
	nd_halos = calc_number_densities(halos[af_criteria], 125)

	# Conduct the abundance matching
	catalog = af.match(nd_halos)

	# A luminosity cutoff to use for the correlation function. We will pick -20 to start
	sub_catalog = catalog<mag_cut
	x = halos['x'][sub_catalog]
	y = halos['y'][sub_catalog]
	z = halos['z'][sub_catalog]

	# Generate rbins so that the average falls at r_p_data
	rbins = np.zeros(len(r_p_data)+1)
	rbins[1:-1] = 0.5*(r_p_data[:-1]+r_p_data[1:])
	rbins[0] = 2*r_p_data[0]-rbins[1]
	rbins[-1] = 2*r_p_data[-1]-rbins[-2]

	# Calculate the projected correlation function
	wp_results = wp(box_size, pimax, nthreads, rbins, x, y, z, verbose=False, 
		output_rpavg=True)

	# Extract the results
	wp_binned = np.zeros(len(wp_results))
	for i in range(len(wp_results)):
	    wp_binned[i] = wp_results[i][3]

	return wp_binned




