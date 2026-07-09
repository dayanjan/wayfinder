# Python -> R Interop (Part D)

The dataframe `persistent_df` was built in the **Python kernel** (Part C), written to a handoff CSV, and read into a **separate R session** where it was rendered with **ggplot2**.

- Rows received in R: 30
- Columns: group, x, y, z
- Plot: `python_to_r_plot.png` — scatter of `x` vs `y` colored by `group`, with per-group linear fits.

Kernels are separate processes that share only the workspace filesystem, so the handoff is via a CSV file (`handoff/persistent_df_for_r.csv`); the plot is genuine ggplot2 output from R.

