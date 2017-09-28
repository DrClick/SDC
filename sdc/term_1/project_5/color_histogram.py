import numpy as np

def color_hist(img, bins=32, bins_range=(0,256)):
    def hist_channel(channel):
        hist = np.histogram(img[:,:,channel], bins=bins, range=bins_range)
        data, bin_edges = hist
        bin_centers = bin_centers = (bin_edges[1:]  + 
                                     bin_edges[0:len(bin_edges)-1])/2
        return data, bin_centers
    
    output = []
    for channel in range(3):
        output.append(hist_channel(channel))
        
    return output
