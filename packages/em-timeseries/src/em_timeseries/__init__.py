"""Shared, semantics-agnostic time series structures.

Metric names, time bases, payload encodings and grid math know nothing about
forecasts, observations or decisions; concrete services layer their own
semantics on top. ORM mixins (em_timeseries.orm) are registry-agnostic and
must be attached to each service's own declarative Base.
"""
