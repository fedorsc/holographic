import numpy as np
import matplotlib.pyplot as plt
from hrr import HRR

class Approximation:

    fn = None
    T = None

    def __init__(self, fn=None, size=1000):
        self.fn = fn
        HRR.reset_kernel()
        if size is not None:
            HRR.set_size(size)
        else:
            HRR.set_size(HRR.size)

    def learn(self, input_range, output_range, n_samples=200, fn=None, stddev=0.03, use_incremental=True):
        if fn is not None:
            self.fn = fn
            HRR.reset_kernel()
        #HRR.input_range = np.array([in_range[0], in_range[1]])
        HRR.stddev = stddev
        # create n_samples evenly spaced sampling points for input space
        A = np.linspace(float(input_range[0]), float(input_range[1]), n_samples)
        #print("A: {}".format(A))
        if use_incremental:
            # initialize T
            B_0 = self.fn(A[0])
            self.T = HRR(B_0, valid_range=output_range) % HRR(A[0], valid_range=input_range)
            # sample function and sequentially update the approximation vector
            for A_i in A[1:]:
                B_i = self.fn(A_i)  # evaluate ith sample
                self.T = self.T ** (HRR(B_i, valid_range=output_range) % HRR(A_i, valid_range=input_range))  # update T
        else:
            samples = np.empty((n_samples, HRR.size), dtype=float)
            for i, A_i in enumerate(A):
                B_i = self.fn(A_i)  # evaluate ith sample
                HRR_A = HRR(A_i, valid_range=input_range)
                HRR_B = HRR(B_i, valid_range=output_range)
                samples[i] = (HRR_B % HRR_A).memory  # probe HRR
                #HRR_A.plot(HRR_A.reverse_permute(HRR_A.memory))
                #HRR_B.plot(HRR_B.reverse_permute(HRR_B.memory))
                #HRR_B.plot(HRR_B.reverse_permute(samples[i]))
            self.T = HRR(0, generator=samples)

        #self.T.plot()
        #print("learn: {}".format(self.T.memory))

    def plot_result(self, input_range, output_range, n_samples=10):
        X = np.linspace(input_range[0], input_range[1], n_samples)
        Y_hrr = np.empty(n_samples, dtype=float)
        Y_hrr2 = np.empty(n_samples, dtype=float)
        Y_hrrsupp = np.empty(n_samples, dtype=float)
        Y_np = np.empty(n_samples, dtype=float)
        for i, x in enumerate(X):
            A = HRR(x, valid_range=input_range)
            B = A * self.T
            #A.plot(A.reverse_permute(A.memory))
            #B.plot(B.reverse_permute(B.memory))
            temp = B.decode(return_dict=True, decode_range=output_range)
            if len(temp) > 1:
                Y_hrr[i] = temp.keys()[1]
                Y_hrr2[i] = temp.keys()[0]
            elif len(temp) > 0:
                Y_hrr[i] = temp.keys()[0]
                Y_hrr2[i] = temp.keys()[0]
            else:
                Y_hrr[i] = np.nan
                Y_hrr2[i] = np.nan
            if len(temp) > 1:
                temp = B.decode(return_dict=False, suppress_value=x, decode_range=output_range)
                #print("suppress_value: {}".format(temp))
                Y_hrrsupp[i] = temp
            else:
                Y_hrrsupp[i] = np.nan
            #Y_hrr[i] = temp
            Y_np[i] = self.fn(x)
            print("HRR: f({}) = 2nd({}) 1st({}) suppr({}) / truth: {} error: {}".format(x, Y_hrr[i], Y_hrr2[i], Y_hrrsupp[i], Y_np[i], Y_hrrsupp[i] - Y_hrr[i]))
        plt.figure()
        h_np, = plt.plot(X, Y_np, 'g', label="Ground truth")
        h_hrr, = plt.plot(X, Y_hrr, 'cx--', label="2nd peak if avail")
        h_hrr2, = plt.plot(X, Y_hrr2, 'bx--', label="1st peak")
        h_suppr, = plt.plot(X, Y_hrrsupp, 'rx-', label="Suppressed input x")
        plt_handles = [h_np, h_hrr, h_hrr2, h_suppr]
        plt.legend(handles=plt_handles, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        plt.show()

