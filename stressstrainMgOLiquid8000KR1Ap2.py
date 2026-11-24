# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.4
#   kernelspec:
#     display_name: cohen_env
#     language: python
#     name: cohen_env
# ---

# %%
# cd /resnick/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/8000K/Viscosity/54671682

# %%
import matplotlib.pyplot as plt
from matplotlib import rcParamsDefault
import numpy as np
# %matplotlib inline
import math


# %%
# load data
def data_loader(fname):
    import numpy as np
    with open(fname, 'r') as f:
        header = f.readline().strip()  # Read the first line (header)
        data = np.loadtxt(f) # loadtxt can take a file object
    step = data[2000:, 0]
    s13 = data[2000:, 10]
    e13 = data[2000:, 12]
    print (header)
    return step,s13,e13,


# %%
import glob
path = "./stressstrain*.dat"
filename = glob.glob(path)[0]
steps, stress, strain = data_loader(filename)

# %%
# scale
rdata = np.zeros((len(steps), 2))
rdata[:,0] = strain
rdata[:,1] = -stress
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(rdata)
data = scaler.transform(rdata)

# %%
plt.figure()
ax = plt.gca()
ax.set_xlim([0, 5000])
#ax.set_ylim([0, 1e8])
plt.plot(data)
plt.show()

# %%
# phase difference determination
plt.figure(figsize=(4,4))
plt.title('Phase diagram')
plt.scatter(data[0:500,0],data[0:500,1])
plt.show()

# %%
c = np.cov(np.transpose(data))
print('cov: ', c)
phi = np.arccos(c[0,1] )
print('phase estimate (radians): ', phi, '(degrees): ', phi / math.pi * 180)

# %%
tandelta=math.tan(phi)
Q=1/math.tan(phi)
print('tan delta: ', tandelta, ' Q: ',Q)

# %%
n=len(strain); print(n)

# %%
#addzeros=np.zeros(len(stress))

# %%
#stress=np.append(stress,addzeros)
#strain=np.append(strain,addzeros)

# %%
from scipy import signal
from scipy.fft import fft, ifft
from scipy.optimize import curve_fit
from scipy.integrate import cumulative_trapezoid, simpson
from scipy.constants import physical_constants as pc
from scipy.stats import linregress

# %%
# phase difference determination
plt.figure(figsize=(4,4))
plt.title('Stress vs Strain')
#plt.plot(np.real(stresstrans))
plt.plot(strain,-stress)
#ax = plt.gca()
#ax.set_xlim([0, 500])
#ax.set_ylim([0, 1e8])
plt.show()

# %%
result=linregress(strain,-stress)

# %%
print(result)

# %%
#window=np.zeros((len(strain)))
#window[:]=signal.get_window(('gaussian',len(strain)/10),len(strain))

# %%
#straintrans=fft(strain*window,norm='forward')
#stresstrans=fft(stress*window,norm='forward')
straintrans=fft(strain,norm='forward')
stresstrans=fft(stress,norm='forward')

# %%
# phase difference determination
plt.figure(figsize=(4,4))
plt.title('Strain Transform')
plt.plot(np.real(straintrans))
plt.plot(-np.imag(straintrans))
ax = plt.gca()
ax.set_xlim([0,25])
#ax.set_ylim([-0.1, 0.1])
plt.show()

# %%
print(straintrans[90:110])

# %%
strainfreqmag=np.max(np.imag(-straintrans[90:150]))
print(strainfreqmag,np.argmax(-straintrans[90:200]))
strainfreq=np.argmax(-straintrans[90:200])*1e15/10/n
print("Freq: ",f"{strainfreq:.2e} Hz, or ",f"{strainfreq*1e-12:.0e} per ps")
print(n)

# %%
np.max(np.imag(stresstrans[90:150]))

# %%
np.max(np.real(stresstrans))

# %%
np.max(np.imag(stresstrans))/np.max(np.imag(straintrans))

# %%
# phase difference determination
plt.figure(figsize=(4,4))
plt.title('Stress Transform')
plt.plot(np.real(stresstrans))
#plt.plot(np.imag(stresstrans))
ax = plt.gca()
ax.set_xlim([90,150])
#ax.set_ylim([0, 1e8])
plt.show()
stressfreq=np.argmax(-stresstrans[1:int(n/2)])
print(stressfreq)

# %%
fig, ax = plt.subplots()
line_strain, = ax.plot(-stress/10000, label='Stress GPa')
line_stress, = ax.plot(strain, label='Strain')
ax.legend(handles=[line_strain, line_stress])
plt.title('Strain and Stress')
import matplotlib.ticker as ticker
ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*0.1))
ax.xaxis.set_major_formatter(ticks)
ax = plt.gca()
ax.set_xlim([0, 2000])
ax.set_xlabel("time (ps)")
plt.show()

# %%
eta=np.max(np.real(stresstrans[90:150]*1e12/10000))/(strainfreq)
freq=strainfreq
print(f"{eta:.2e} Pa s at {freq:0.0e} Hz")

# %%
np.max(np.real(stresstrans[10:200]))

# %%
np.argmax(np.real(stresstrans[80:200]))

# %%
plt.figure(figsize=(4,4))
plt.title('Stress Transform')
plt.plot(np.real(stresstrans))
ax = plt.gca()
ax.set_xlim([20, 250])
#ax.set_ylim([0, 1e8])
plt.show()

# %%

# %%

# %%
