import math
import pandas as pd
from statistics import NormalDist

z = NormalDist().inv_cdf


def n_per_group(sigma: float, mde: float, alpha: float = 0.05, power: float = 0.8,
                comparisons: int = 1) -> int:
    """Клиентов на КАЖДУЮ группу, чтобы заметить эффект mde с заданной мощностью."""
    za = z(1 - alpha / (2 * comparisons))
    # Второй квантиль отвечает за мощность. Какой у него аргумент?
    zb = z(power)
    return math.ceil(2 * (za + zb) ** 2 * sigma ** 2 / mde ** 2)

def mde_for_n(
    sigma: float, 
    n: int, 
    alpha: float = 0.05, 
    power: float = 0.8, 
    comparisons: int = 1
) -> float:
    """Минимальный детектируемый эффект (MDE) для заданного размера группы n."""
    if n <= 0:
        raise ValueError("Размер группы n должен быть больше 0")
        
    za = z(1 - alpha / (2 * comparisons))
    zb = z(power)
    
    return (za + zb) * sigma * math.sqrt(2 / n)

def cuped(y, x):
    # метрика после поправки CUPED и theta; y и x — pandas.Series одной длины
    theta = y.cov(x) / x.var()
    return y - theta * (x - x.mean()), theta

from scipy import stats

from scipy import stats   # добавьте в начало файла, если ещё нет

def diff_ci(t: pd.Series, c: pd.Series, alpha: float = 0.05) -> dict:
    """Разность средних test − control, её 95 % интервал Уэлча и p-значение."""
    d = t.mean() - c.mean()
    n_t, n_c = len(t), len(c)
    v_t, v_c = t.var(), c.var()
    se = (v_t / n_t + v_c / n_c) ** 0.5

    # степени свободы Уэлча
    num = (v_t / n_t + v_c / n_c) ** 2
    den = (v_t / n_t) ** 2 / (n_t - 1) + (v_c / n_c) ** 2 / (n_c - 1)
    df = num / den

    t_stat = d / se
    p = 2 * stats.t.sf(abs(t_stat), df=df)
    t_crit = stats.t.ppf(1 - alpha / 2, df=df)
    return {"diff": d, "lo": d - t_crit * se, "hi": d + t_crit * se, "p": p}

def srm_pvalue(sizes) -> float:
    # p-значение chi2 согласия с равными долями для 2 или 3 групп
    n = sum(sizes)
    exp = n / len(sizes)
    chi2 = sum((s - exp) ** 2 / exp for s in sizes)
    if len(sizes) == 2:
        return math.erfc(math.sqrt(chi2 / 2))
    if len(sizes) == 3:
        return math.exp(-chi2 / 2)
    raise ValueError("для 4 и более групп — scipy.stats.chisquare")