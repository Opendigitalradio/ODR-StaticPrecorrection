from scipy import signal
import numpy as np
import pandas as pd
from tqdm import tqdm
import src.gen_source as gs
import src.dab_util as du

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


def test_using_aligned_pair(sample_orig=r'../data/orig_rough_aligned.dat', sample_rec =r'../data/recored_rough_aligned.dat', length = 10240, max_size = 1000000):
    res = []
    for i in tqdm(range(100)):
        start = np.random.randint(50, max_size)
        r = np.random.randint(-50, 50)

        s1 = du.fromfile(sample_orig, offset=start+r, length=length)
        s2 = du.fromfile(sample_rec, offset=start, length=length)

        res.append({'offset':r,
                    '1':r - du.lag_upsampling(s2, s1, n_up=1),
                    '2':r - du.lag_upsampling(s2, s1, n_up=2),
                    '3':r - du.lag_upsampling(s2, s1, n_up=3),
                    '4':r - du.lag_upsampling(s2, s1, n_up=4),
                    '8':r - du.lag_upsampling(s2, s1, n_up=8),
                    '16':r - du.lag_upsampling(s2, s1, n_up=16),
                    '32':r - du.lag_upsampling(s2, s1, n_up=32),
                    })
    df = pd.DataFrame(res)
    df = df.reindex_axis(sorted(df.columns), axis=1)
    print(df.describe())

def test_subsample_alignment(sample_orig=r'../data/orig_rough_aligned.dat',
        sample_rec =r'../data/recored_rough_aligned.dat', length = 10240, max_size = 1000000):
    res1 = []
    res2 = []
    for i in tqdm(range(10)):
        start = np.random.randint(50, max_size)
        r = np.random.randint(-50, 50)

        s1 = du.fromfile(sample_orig, offset=start+r, length=length)
        s2 = du.fromfile(sample_rec, offset=start, length=length)

        res1.append(du.lag_upsampling(s2, s1, 32))

        s1_aligned, s2_aligned = du.subsample_align(s1,s2)

        res2.append(du.lag_upsampling(s2_aligned, s1_aligned, 32))

    print("Before subsample alignment: lag_std = %.2f, lag_abs_mean = %.2f" % (np.std(res1), np.mean(np.abs(res1))))
    print("After subsample alignment: lag_std = %.2f, lag_abs_mean = %.2f" % (np.std(res2), np.mean(np.abs(res2))))

print("Align using upsampling")
for n_up in [1, 2, 3, 4, 7, 8, 16]:
   correct_ratio = test_phase_offset(lambda x,y: du.lag_upsampling(x,y,n_up), tol=1./n_up)
   print("%.1f%% of the tested offsets were measured within tolerance %.4f for n_up = %d" % (correct_ratio * 100, 1./n_up, n_up))
test_using_aligned_pair()

print("Phase alignment")
test_subsample_alignment()
