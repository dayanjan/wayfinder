# Claude Science capability audit — executed R source (Part D).
# Python -> R interop: read the handoff CSV written by the Python kernel and
# render persistent_df with ggplot2. CPU-only, no external data.

suppressMessages(library(ggplot2))

df <- read.csv("handoff/persistent_df_for_r.csv")
stopifnot(nrow(df) == 30, all(c("group", "x", "y", "z") %in% colnames(df)))

p <- ggplot(df, aes(x = x, y = y, color = group)) +
  geom_point(size = 3, alpha = 0.85) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 0.6) +
  labs(title = "Python to R interop: persistent_df",
       subtitle = "Dataframe created in the Python kernel, plotted in R with ggplot2",
       x = "x", y = "y", color = "group") +
  theme_minimal(base_size = 13)

ggsave("cs_capability_audit_db/python_to_r_plot.png", plot = p,
       width = 7, height = 5, dpi = 300)
