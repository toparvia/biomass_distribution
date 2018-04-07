
# coding: utf-8

# In[1]:

#Load dependencies

import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0,'../statistics_helper/')
from CI_helper import *
from excel_utils import *
pd.options.display.float_format = '{:,.1e}'.format


# # Estimating the biomass of plants
# In order to estimate the biomass of plants, we rely on data generated by [Erb et al.](https://doi.org/10.1038/nature25138), which generated seven different estimates of the global biomass of plants. The seven estimates are:

# In[2]:

data = pd.read_excel('plant_data.xlsx', skiprows=1)
data['Total biomass estimate [g C]'] = data['Total biomass estimate [g C]'].astype(float)
data


# As best estimate of the total biomass of plants, we use the value reported in Erb et al. of 450 Gt C.

# In[3]:

best_estimate = 450e15
print('Our best estimate for the biomass of plants is ≈%.0f Gt C' %(best_estimate/1e15))


# ## Marine plants
# We estimate the total biomass of seagrass from data reported in [Fourqurean et al.](https://doi.org/10.1038/ngeo1477). Fourqurean report an average carbon density in living biomass of seagrass at ≈250 g C $m^{-2}$. They also estimate the total area of seagrass is ≈300,000-600,000 $km^2$. We multiply the average biomass denisty of plants by the average area covered by seagrass to generate our best estimate of the total biomass of seagrass.

# In[4]:

# Mean biomass concentration of seagrasses
mean_biomass_conc_seagrass =250

# Mean area covered by seagrasses
mean_area = np.average([3e11,6e11])

best_seagrass = mean_biomass_conc_seagrass*mean_area
print('Our best estimate for the total biomass of seagrasses is ≈%.1f Gt C' %(best_seagrass/1e15))


# For macroalgea, we rely on a range of estimates for the total biomass of macroalgae from De Vooys, which reports 0.0075 Gt C and Cherpy-Roubaud & Sournia which report 2.55 Gt C. We use the geometric mean of this range as a crude estimate of the biomass of macroalgae:

# In[5]:

best_macroalgae = gmean([0.0075e15,2.55e15])
print('Our best estimate for the total biomass of seagrasses is ≈%.1f Gt C' %(best_macroalgae/1e15))


# # Uncertainty analysis
# As noted in the plants section in the Supplementary Information, one possible strategy to assess the uncertainty associated with the estimate of the total biomass of plants is to calculate the 95% confidence interval around the best estimate:

# In[6]:

estimate_CI = geo_CI_calc(data['Total biomass estimate [g C]'])
print('The 95 percent confidence interval around our best estimate for the total biomass of plants is ≈%.1f-fold' %estimate_CI)


# In order to account for additional sources of uncertainty not captured by calculating the 95% confidence interval, we use the ratio between uper and lower most estimates relative to our best estimate as our best projection for the uncertainty associated with our estimate of the total biomass of plants:

# In[7]:

upper_CI = data['Total biomass estimate [g C]'].max()/best_estimate
lower_CI = best_estimate/data['Total biomass estimate [g C]'].min()

mul_CI = np.max([upper_CI,lower_CI])

print('Our best projection for the uncertainty associated with the estimate of the total biomass of plants is ≈%.1f-fold' %mul_CI)


# # Total number of invididuals
# We estimate the total number of trees, based on a recent study ([Crowther et al.](http://dx.doi.org/10.1038/nature16178)). Include all plant species will definitely increase the estimate dramatically, but due to the high diversity of species and characteristic sizes of different plant species, it is very difficult to estimate the total number of plants in the biosphere. Crowther et al. estimate ≈$3×10^{12}$ trees.

# In[8]:

tot_tree_num = 3e12


# In[9]:

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Plants','Plants'), 
               col=['Biomass [Gt C]', 'Uncertainty','Total uncertainty'],
               values=[best_estimate/1e15,mul_CI,mul_CI],
               path='../results.xlsx')

# Feed results to Fig. 2C
# Feed seagrass biomass
update_fig2c(row=21,col=1,values=best_seagrass/1e15, path='../results.xlsx')

# Feed macroalgae biomass
update_fig2c(row=22,col=1,values=best_macroalgae/1e15, path='../results.xlsx')

# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Plants','Plants'), 
               col=['Number of individuals'],
               values=tot_tree_num,
               path='../results.xlsx')

