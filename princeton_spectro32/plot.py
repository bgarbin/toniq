# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 18:17:28 2019

@author: manip
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
data = np.loadtxt('./test_winspec.txt')
plt.plot(data)
#plt.plot()