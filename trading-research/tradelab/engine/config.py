"""Risk configuration. Every limit comes from one TOML file you own.

The engine refuses to run if a limit is missing, out of range, or if you have
not set `config_reviewed = true` after choosing your own numbers.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    pass


# key -> (min, max) inclusive, for numeric limits
NUMERIC_LIMITS: dict[str, tuple[float, float]] = {
    "account_equity": (1, 1e12),
    "risk_per_trade_pct": (0.01, 5),
    "max_long_position_pct": (0.1, 100),
    "max_short_position_pct": (0.1, 100),
    "max_gross_exposure_pct": (1, 300),
    "max_order_notional": (1, 1e12),
    "max_open_positions": (1, 200),
    "max_daily_loss_pct": (0.1, 50),
    "max_drawdown_pct": (0.5, 90),
    "price_tolerance_pct": (0.1, 20),
    "max_price_age_days": (0, 30),
    "max_short_interest_pct": (1, 100),
    "earnings_blackout_days": (0, 30),
    "atr_stop_multiple": (0.5, 10),
    "trail_atr_multiple": (0.5, 10),
    "time_stop_days": (1, 3650),
    "vix_risk_on_level": (5, 100),
    "vix_risk_off_level": (5, 100),
    "global_shock_pct": (0.5, 20),   # block new longs if a watched index falls this much in a day
}


@dataclass(frozen=True)
class Config:
    config_reviewed: bool
    allowlist: frozenset[str]
    block_longs_in_risk_off: bool
    block_shorts_in_risk_on: bool
    targets: tuple[tuple[float, float], ...]  # (R multiple, fraction of initial qty)
    values: dict[str, float]

    def __getattr__(self, name: str) -> float:
        try:
            return self.__dict__["values"][name]
        except KeyError as exc:
            raise AttributeError(name) from exc


def parse_config(data: dict) -> Config:
    if data.get("config_reviewed") is not True:
        raise ConfigError("set config_reviewed = true after choosing your own limits")

    values: dict[str, float] = {}
    for key, (lo, hi) in NUMERIC_LIMITS.items():
        if key not in data:
            raise ConfigError(f"missing limit: {key}")
        val = data[key]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            raise ConfigError(f"{key} must be a number")
        if not lo <= val <= hi:
            raise ConfigError(f"{key}={val} outside allowed range {lo}..{hi}")
        values[key] = float(val)

    if values["vix_risk_on_level"] >= values["vix_risk_off_level"]:
        raise ConfigError("vix_risk_on_level must be below vix_risk_off_level")

    allow = data.get("allowlist")
    if not isinstance(allow, list) or not allow or not all(isinstance(t, str) for t in allow):
        raise ConfigError("allowlist must be a non-empty list of tickers")

    raw_targets = data.get("targets")
    if not isinstance(raw_targets, list) or not raw_targets:
        raise ConfigError("targets must be a non-empty list of [r_multiple, fraction]")
    targets = []
    for t in raw_targets:
        if not (isinstance(t, list) and len(t) == 2 and t[0] > 0 and 0 < t[1] <= 1):
            raise ConfigError("each target must be [r_multiple > 0, 0 < fraction <= 1]")
        targets.append((float(t[0]), float(t[1])))
    if sum(f for _, f in targets) > 1:
        raise ConfigError("target fractions must sum to at most 1")

    return Config(
        config_reviewed=True,
        allowlist=frozenset(t.upper() for t in allow),
        block_longs_in_risk_off=bool(data.get("block_longs_in_risk_off", True)),
        block_shorts_in_risk_on=bool(data.get("block_shorts_in_risk_on", True)),
        targets=tuple(targets),
        values=values,
    )


def load_config(path: str | Path) -> Config:
    with open(path, "rb") as fh:
        return parse_config(tomllib.load(fh))
