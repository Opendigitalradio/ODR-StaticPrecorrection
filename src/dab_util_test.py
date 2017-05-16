from scipy import signal
import numpy as np
import src.gen_source as gs
reload(gs)
import src.dab_util as du
reload(du)

def gen_test_signals(oversampling=4, sample_offset_float=0):
    off = int(sample_offset_float)
    phi_samples = sample_offset_float - off
    phi = phi_samples*360/oversampling

    s1 = np.zeros((1024))
    s1[256:768] = gs.gen_sin(512, oversampling, 0)
    s2 = np.zeros((1024))
    s2[256+off:768+off] = gs.gen_sin(512, oversampling, phi)

    return s1, s2

def test_phase_offset(lag_function, tol):
    def r():
        return np.random.rand(1)*100-50
    res = []
    for i in range(100):
        off = r()
        s1, s2 = gen_test_signals(
            oversampling=4, sample_offset_float=off)

        off_meas = lag_function(s2, s1)
        res.append(np.abs(off-off_meas)<tol)
    return np.mean(res)

for n_up in [1, 2, 3, 4, 7, 8, 16]:
   correct_ratio = test_phase_offset(lambda x,y: du.lag_upsampling(x,y,n_up), tol=1./n_up)
   print("%.1f%% of the tested offsets were measured within tolerance %.4f for n_up = %d" % (correct_ratio * 100, 1./n_up, n_up))

