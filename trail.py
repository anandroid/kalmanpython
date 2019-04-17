from scipy.stats import norm

# generate random numbers from N(0,1)


import matplotlib
import matplotlib.pyplot as plt
import math
# for latex equations
from IPython.display import Math, Latex
# for displaying images
from IPython.core.display import Image

import scipy.stats

import seaborn as sns
# settings for seaborn plotting style
sns.set(color_codes=True)
# settings for seaborn plot sizes
sns.set(rc={'figure.figsize':(5,5)})


data_normal = norm.rvs(size=100,loc=-72,scale=1)
ax = sns.distplot(data_normal,
                  bins=10,
                  kde=True,
                  color='skyblue',
                  hist_kws={"linewidth": 15,'alpha':1})
ax.set(xlabel='Normal Distribution', ylabel='Frequency')

#plt.show()

#scipy.stats.norm(-73, 1)


print(math.log(scipy.stats.norm(-73, 2).pdf(-76)))

print (math.log(0.4))



