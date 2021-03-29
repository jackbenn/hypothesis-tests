
from scipy.special import logit, expit
from scipy import stats
import numpy as np



def plot_pvalues(ax, data=None, func=None, dist=None):
    lower, upper = -0.25, 1.25
    xpts = np.linspace(lower, upper, 500)
    if dist is not None:
        ax.plot(xpts,
                dist.pdf(xpts),
                color='r',
                label='actual')
    if func is None:
        ax.hist(data,
                bins=np.linspace(0, 1, 11),
                density=True)
    else:
        kde = func(data)
        ax.plot(xpts,
                kde(xpts),
               label='kde')
    ax.set_ylim(ymin=0)
    ax.set_xlim(lower, upper)
    if data is not None:
        for i, datum in enumerate(data):
            ax.axvline(datum,
            color='k',
            lw=1,
            alpha=0.2,
            label='data' if i==0 else None)
    ax.legend()


def transforming_bounded_kde(data, minimum=0, maximum=2):
    """Return a gaussian kde function bounded between two points.
    Note that it doesn't handle when x is on the edge. 
    """
    if (np.any(np.less_equal(data, minimum)) or
        np.any(np.greater_equal(data, maximum))):
        raise ValueError("data must be strictly between minimum and maximum")
    diff = maximum - minimum
    kde = stats.gaussian_kde(logit((data - minimum)/diff))
    def transformed_kde(x):
        x = (x-minimum)/diff
        return kde(logit(x))/(x*(1-x))/diff
    return transformed_kde

# nb this assume the original kde decays to zero
# by -1 and 2, so doesn't reflect of both ends
def reflecting_bounded_kde(data):
    """Return a gaussian kde function bounded between """
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
