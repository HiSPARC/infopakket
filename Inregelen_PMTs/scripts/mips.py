from pylab import *


figure()
x = linspace(0, 10, 300)
th_signal = []
signal = zeros(x.shape)
for N in range(1, 15):
    scale = 1. / N ** 3
    pdf = scale * normpdf(x, N, sqrt(N) * .35)
    plot(x, pdf)
    signal += pdf
    th_signal.extend(int(100 * scale) * [N])

plot(x, signal)
yscale('log')
ylim(ymin=1e-3)

figure()
hist(th_signal, bins=linspace(0, 10, 100), histtype='step')
