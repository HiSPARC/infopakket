from pylab import *
from artist import MultiPlot


multiplot = MultiPlot(3, 1, axis='semilogy', width=r'.5\linewidth')

#figure()
subplot = multiplot.get_subplot_at(1, 0)
subplot2 = multiplot.get_subplot_at(2, 0)
x = linspace(0, 10, 50)
th_signal = []
signal = zeros(x.shape)
for N in range(1, 15):
    scale = 1. / N ** 3
    pdf = 80 * scale * normpdf(x, N, sqrt(N) * .35)
#    plot(x, pdf)
    subplot.plot(x, pdf, mark=None)
    subplot2.plot(x, pdf, mark=None, linestyle='gray')
    signal += pdf
    th_signal.extend(int(100 * scale) * [N])

subplot = multiplot.get_subplot_at(2, 0)
#plot(x, signal)
subplot.plot(x, signal, mark=None)
#yscale('log')
#ylim(ymin=1e-3)

#figure()
#hist(th_signal, bins=linspace(0, 10, 100), histtype='step')

n, bins = histogram(th_signal, bins=linspace(0, 10, 100))
n = where(n == 0, 1e-1, n)
subplot = multiplot.get_subplot_at(0, 0)
subplot.histogram(n, bins)

multiplot.show_xticklabels(2, 0)
multiplot.show_yticklabels_for_all([(0, 0), (1, 0), (2, 0)])
multiplot.set_xlabel('Number of particles')
multiplot.set_ylabel('Counts')
multiplot.set_ylimits_for_all(min=1e-1, max=2e2)
multiplot.set_xlimits_for_all(min=0, max=10)

multiplot.save_as_pdf('preview')
