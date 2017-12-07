import pylab

from artist import MultiPlot


def plot_spectrum_componenten():
    """Plot voor componenten pulshoogte spectrum"""

    multiplot = MultiPlot(3, 1, axis='semilogy', width=r'0.5\linewidth')

    pylab.clf()
    subplot0 = multiplot.get_subplot_at(0, 0)
    subplot1 = multiplot.get_subplot_at(1, 0)
    subplot2 = multiplot.get_subplot_at(2, 0)
    x = pylab.linspace(1e-10, 11, 200)
    th_signal = []
    signal = pylab.zeros(x.shape)
    for N in range(1, 15):
        scale = 100. / N ** 3
        pdf = 80 * scale * pylab.normpdf(x, N, pylab.sqrt(N) * 0.35)
        # pylab.plot(x, pdf)
        subplot1.plot(x, pdf, mark=None)
        # subplot1.add_pin('%d MIP' % N, 'above right', x=N, use_arrow=True,
        #                  style='lightgray')
        subplot2.plot(x, pdf, mark=None, linestyle='lightgray')
        signal += pdf
        th_signal.extend(int(100 * scale) * [N])

    gammas = 1e2 * x ** -3
    subplot1.plot(x, gammas, mark=None)
    subplot2.plot(x, gammas, mark=None, linestyle='lightgray')

    signal += gammas
    pylab.plot(x, signal)
    pylab.plot(x, gammas)
    subplot2.plot(x, signal, mark=None)
    pylab.yscale('log')
    pylab.ylim(ymin=1)

    n, bins = pylab.histogram(th_signal, bins=pylab.linspace(0, 11, 100))
    n = pylab.where(n == 0, 1e-10, n)
    subplot0.histogram(n, bins)

    multiplot.show_xticklabels_for_all([(0, 0), (2, 0)])
    multiplot.set_xticks_for_all([(0, 0), (2, 0)], range(20))
    # multiplot.show_yticklabels_for_all([(0, 0), (1, 0), (2, 0)])
    multiplot.set_xlabel('Aantal deeltjes')
    multiplot.set_ylabel('Aantal events')
    multiplot.set_ylimits_for_all(min=1, max=1e5)
    multiplot.set_xlimits_for_all(min=0, max=10.5)

    multiplot.save('spectrum_componenten')


def plot_afstelling_pmt():
    """Plot voor afstellen spanning"""

    multiplot = MultiPlot(1, 3, width=r'0.4\linewidth')

    x = pylab.linspace(1e-10, 11, 200)

    signal = pylab.zeros(x.shape)

    for N in range(1, 15):
        scale = 100. / N ** 3
        pdf = 80 * scale * pylab.normpdf(x, N, pylab.sqrt(N) * 0.35)
        signal += pdf

    gammas = 1e2 * x ** -3
    signal += gammas

    p = multiplot.get_subplot_at(0, 0)
    v = x * 35
    p.plot(v, pylab.where(v >= 30, signal, 1), mark=None)
    p.draw_vertical_line(200, linestyle='gray')
    p.set_label(r"$V_\mathrm{PMT}$ te laag")

    p = multiplot.get_subplot_at(0, 1)
    v = x * 200
    p.plot(v, pylab.where(v >= 30, signal, 1), mark=None)
    p.draw_vertical_line(200, linestyle='gray')
    p.set_label(r"$V_\mathrm{PMT}$ correct")

    p = multiplot.get_subplot_at(0, 2)
    v = x * 400
    p.plot(v, pylab.where(v >= 30, signal, 1), mark=None)
    p.draw_vertical_line(200, linestyle='gray')
    p.set_label(r"$V_\mathrm{PMT}$ te hoog")

    multiplot.set_xlabel(r"Pulseheight [\si{\milli\volt}]")
    multiplot.set_ylabel("Counts")
    multiplot.set_xlimits_for_all(min=0, max=1000)
    multiplot.set_ylimits_for_all(min=1)
    multiplot.show_xticklabels_for_all()
    multiplot.set_xticklabels_position(0, 1, 'top')
    multiplot.set_yticks_for_all(ticks=None)
    multiplot.save('afstelling_pmt')


if __name__ == "__main__":
    plot_spectrum_componenten()
    plot_afstelling_pmt()
