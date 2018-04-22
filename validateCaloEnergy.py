# VALIDATE RANGE vs. CALORIMETRY ENERGY

# invert Recombination Modified Box Model to get dE/dx from dQ/dx

# argon density [g/cm^3]
rho = 1.396
# electric field [kV/cm]
efield = 0.273
# ionization energy [MeV/e-]
Wion = 23.6*(10**(-6))

fModBoxA = 0.93
fModBoxB = 0.562

def ModBoxInverse(dqdx):
    dedx = (np.exp(fModBoxB * Wion * dqdx ) - fModBoxA) / fModBoxB
    return dedx

from scipy.interpolate import spline

pdg_rr_v = []
pdg_dedx_v = []
pdg_ke_v = []
pdg_rr_fit_v = []
pdg_dedx_fit_v = []
pdg_ke_fit_v = []

fin = open('/home/david//Dropbox/Neutrinos/Varie/michelCalib/mutable.txt')
rho = 1.396

for line in fin:
    words = line.split()
    pdg_rr_v.append(   float(words[-1])/rho )
    pdg_dedx_v.append( float(words[2]) *rho )
    pdg_ke_v.append(   float(words[0])      )
    
    
pdg_rr_fit_v   = np.linspace(1,1000,10000)
pdg_dedx_fit_v = spline(pdg_rr_v,pdg_dedx_v,pdg_rr_fit_v)
pdg_ke_fit_v = spline(pdg_rr_v,pdg_ke_v,pdg_rr_fit_v)


# fiven a RR value, get the energy
def ERange(RR):
    for i in xrange(len(pdg_rr_fit_v)):
        if (RR <= pdg_rr_fit_v[i]):
        return pdg_ke_fit_v[i]
    return -1

def Pitch(x):
    return 0.3/np.abs(x['_pz'])

dfcuts['pitch'] = dfcuts.apply(lambda x : Pitch(x),axis=1)

# elec gain : 200 e-/ADC in MC, 243 in DATA.
def Energy(x,elecgain):
    energy = 0.
    dqdx_v = x['_dqdx_v']
    rr_v   = x['_rr_v']
    for i in xrange(1,len(dqdx_v)):
        dqdx = dqdx_v[i]
        drr  = np.abs(rr_v[i-1]-rr_v[i])
        dedx = ModBoxInverse(dqdx*elecgain)
        energy += drr * dedx
        energy += (np.abs(rr_v[0]-rr_v[1])) * ModBoxInverse(dqdx_v[0]*elecgain)
    return energy
    
    
    dfcuts['energy'] = dfcuts.apply(lambda x : Energy(x,241.), axis=1)
    
def EnergyfromRange(x):
    rrmax = np.max(x['_rr_v'])
    return ERange(rrmax)
