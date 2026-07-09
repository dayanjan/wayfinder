# Figure Self-Correction (Part E)

**v1** (`scatter_v1.png`) plots 20 near-normal points plus one deliberately extreme point, with no annotation. On visual inspection the lone point at the bottom-right is clearly detached from the cluster, but v1 does not mark or explain it.

**Automated check.** Z-scores were computed on both axes over all 21 points; any point with |z| > 3 on either axis is flagged:

- Points flagged: **1**
- Flagged point(s):
  x    y  z_x   z_y
8.5 -7.2 4.16 -3.87

**Correction in v2** (`scatter_v2.png`): the flagged point is drawn with a hollow red ring, labeled with its coordinates and per-axis z-scores, and separated in the legend from the within-3σ points.

Note on method: because the outlier is included in the mean/SD estimate it inflates the spread, yet the point still exceeds 3σ on the x-axis — an outlier extreme enough to survive its own leverage on the threshold. A robust estimator (median/MAD) would flag it even more strongly.
