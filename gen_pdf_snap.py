# this script reads a SNAP CSV file generated using Larry's code and generates 
# a PDF containing one spectrum per page.
# the name of the input CSV file is put in the variable *fname_in*
# the output file is in the same location as the input CSV file, with
# extension .pdf
# the location and name of the output file can be changed and put in the
# variable *fname_out*


fname_in = 'C:\\Users\\gregh\\Downloads\\18Apr22_snap07.csv';

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv

fname_out = fname_in[:-4]+'.pdf';

pp = PdfPages(fname_out);
array = np.loadtxt(fname_in, delimiter=",");
plt.rcParams.update({'font.size': 22});

spclog = 10.*np.log10(array[:,1:]);
idxfinite = np.isfinite(spclog);
maxval = np.max(np.max(spclog[idxfinite]));
minval = np.min(np.min(spclog[idxfinite]));

for k in range(array.shape[-1]-1):
    f = plt.figure(figsize=(21,12));
    ax = f.add_subplot(1,1,1);
    plt.plot(np.linspace(0.,98.304,array.shape[0]),spclog[:,k],linewidth=2,rasterized=True);
    plt.xlabel('frequency [MHz]');
    plt.ylabel('power [dB]');
    plt.grid();
    plt.xlim([0,98.304]);
    plt.ylim([minval,maxval]);
    plt.title('channel # '+str(k));
    plt.tight_layout();
    pp.savefig(f);
    plt.close();

pp.close();
