from pylab import *
from artist import MultiPlot


multiplot = MultiPlot(3, 1, axis='semilogy', width=r'.5\linewidth')

clf()
subplot = multiplot.get_subplot_at(1, 0)
subplot2 = multiplot.get_subplot_at(2, 0)
x = linspace(0, 11, 200)
th_signal = []
signal = zeros(x.shape)
for N in range(1, 15):
    scale = 100. / N ** 3
    pdf = 80 * scale * normpdf(x, N, sqrt(N) * .35)
    #plot(x, pdf)
    subplot.plot(x, pdf, mark=None)
    #subplot.add_pin('%d MIP' % N, 'above right', x=N, use_arrow=True,
    #                style='lightgray')
    subplot2.plot(x, pdf, mark=None, linestyle='lightgray')
    signal += pdf
    th_signal.extend(int(100 * scale) * [N])

gammas = 1e2 * x ** -3
subplot.plot(x, gammas, mark=None)
subplot2.plot(x, gammas, mark=None, linestyle='lightgray')

signal += gammas
plot(x, signal)
plot(x, gammas)
subplot2.plot(x, signal, mark=None)
yscale('log')
ylim(ymin=1)

subplot = multiplot.get_subplot_at(2, 0)
n, bins = histogram(th_signal, bins=linspace(0, 11, 100))
n = where(n == 0, 1e-10, n)
subplot = multiplot.get_subplot_at(0, 0)
subplot.histogram(n, bins)

multiplot.show_xticklabels_for_all([(0, 0), (2, 0)])
multiplot.set_xticks_for_all([(0, 0), (2, 0)], range(20))
#multiplot.show_yticklabels_for_all([(0, 0), (1, 0), (2, 0)])
multiplot.set_xlabel('Aantal deeltjes')
multiplot.set_ylabel('Aantal events')
multiplot.set_ylimits_for_all(min=1, max=1e5)
multiplot.set_xlimits_for_all(min=0, max=10.5)

multiplot.save('spectrum_componenten')
