
from scipy.special import logit, expit
from scipy import stats
import numpy as np



def plot_pvalues(ax, data, show_data=True):
    lower, upper = -0.25, 1.25
    xpts = np.linspace(lower, upper, 500)
    dist = stats.uniform(0, 1)

    if show_data:
        for i, datum in enumerate(data):
            ax.axvline(datum,
            color='k',
            lw=1,
            alpha=0.2,
            label='data' if i==0 else None)
    
    ax.plot(xpts,
            dist.pdf(xpts),
            color='r',
            label='actual')

    kde = reflecting_bounded_kde(data)
    ax.plot(xpts,
            kde(xpts),
            label='kde')
    ax.set_ylim(ymin=0)
    ax.set_xlim(lower, upper)


    ax.legend()

def plot_quantiles(ax, data):

    qq = stats.probplot(data,
                        dist=stats.uniform(0, 1),
                        fit=False)
    ax.scatter(qq[0], qq[1])
    ax.plot([0, 1], [0, 1], 'r')
    ax.set_xlabel('quantiles of U(0, 1)')
    ax.set_ylabel('simulated pvalues')


def reflecting_bounded_kde(data):
    """Return a gaussian kde function bounded between 0 and 1
    reflecting gaussians off either end.
    NB: this assume the original kde decays to zero
    by -1 and 2, so doesn't reflect of both ends.
    """
    kde = stats.gaussian_kde(data)
    def rbkde(x):
        result = np.where
    return lambda x: np.where(x < 0,
                              0,
                              np.where(x > 1,
                                       0,
                                       kde(x)+
                                       kde(-x)+
                                       kde(2-x)))
