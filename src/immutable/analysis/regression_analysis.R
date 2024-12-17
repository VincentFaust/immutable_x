library(readr)
library(dplyr)
library(ggplot2)
library(httpgd)
library(mgcv)
library(boot)
library(parallel)
library(xtable)


setwd("/Users/fitz/Coding/immutable_x/src/immutable/analysis")

# Load the data
orders <- read_csv("orders.csv")

# filtering for only ETH orders
orders_filtered <- orders %>%
    filter(buy_type == "ETH")

# Summarize data: raw totals
user_activity_raw <- orders_filtered %>%
    group_by(user) %>%
    summarise(
        n_orders = n(),
        total_buy_quantity = sum(buy_quantity, na.rm = TRUE)
    )

# Exploratory analysis comparing number of user orders and total buy quantity
ggplot(user_activity_raw, aes(x = n_orders, y = total_buy_quantity)) +
    geom_point(alpha = 0.5, color = "blue") +
    labs(
        title = "Scatter Plot: Number of Orders vs Total Buy Quantity (Raw Values)",
        x = "Number of Orders",
        y = "Total Buy Quantity"
    ) +
    theme_minimal()


# Apply log transformation to response and predictor variables
user_activity <- user_activity_raw %>%
    mutate(
        log_total_buy_quantity = log(total_buy_quantity + 1),
        log_n_orders = log(n_orders + 1)
    )

# Exploratory analysis comparing log-transformed number of user orders and total buy quantity
ggplot(user_activity, aes(x = log_n_orders, y = log_total_buy_quantity)) +
    geom_point(alpha = 0.5, color = "blue") +
    labs(
        title = "Scatter Plot: Log(Number of Orders) vs Log(Total Buy Quantity)",
        x = "Log(Number of Orders)",
        y = "Log(Total Buy Quantity)"
    ) +
    theme_minimal()

# Fit a GAM model to the log-transformed data
gam_model <- gam(log_total_buy_quantity ~ s(log_n_orders), data = user_activity)

# Plot the GAM model
plot(gam_model, pages = 1, shade = TRUE, rug = TRUE)

# Fits a smoothing method of the GAM model to the data for easier interpretation
ggplot(user_activity, aes(x = log_n_orders, y = log_total_buy_quantity)) +
    geom_point(alpha = 0.5) +
    stat_smooth(method = "gam", formula = y ~ s(x), col = "blue") +
    labs(
        title = "GAM: Log(Number of Orders) vs Log(Total Buy Quantity)",
        x = "Log(Number of Orders)",
        y = "Log(Total Buy Quantity)"
    )

# Generate the GAM summary
gam_summary <- summary(gam_model)

# Extract parametric coefficients and smooth terms
parametric_table <- as.data.frame(gam_summary$p.table) # Parametric coefficients
smooth_table <- as.data.frame(gam_summary$s.table) # Smooth terms

# Round values for better display
parametric_table <- round(parametric_table, 5)
smooth_table <- round(smooth_table, 5)


# Export parametric coefficients table
print(
    xtable(parametric_table,
        caption = "Parametric Coefficients of the GAM Model",
        label = "tab:parametric_coeff"
    ),
    file = "gam_parametric_table.tex",
    include.rownames = TRUE,
    include.colnames = TRUE,
    floating = FALSE # Remove the \begin{table} and \end{table} wrappers
)

# Export smooth terms table
print(
    xtable(smooth_table,
        caption = "Significance of Smooth Terms in the GAM Model",
        label = "tab:smooth_terms"
    ),
    file = "gam_smooth_table.tex",
    include.rownames = TRUE
)

# Save summary statistics manually
summary_stats <- paste(
    "R-sq.(adj) =", round(gam_summary$r.sq, 3),
    ", Deviance explained =", round(gam_summary$dev.expl * 100, 1), "%",
    ", GCV =", round(gam_summary$sp.criterion, 6),
    ", Scale est. =", round(gam_summary$scale, 6),
    ", n =", gam_summary$n
)

# Write the summary statistics to a file
writeLines(summary_stats, "gam_summary_stats.tex")

# Checking the GAM model with diagnostic plots
par(mfrow = c(2, 2))
gam.check(gam_model)
par(mfrow = c(1, 1))


# boostrap confidence intervals for the GAM model
bootstrap_gam <- function(data, indices) {
    resampled_data <- data[indices, ]
    gam_model <- gam(log_total_buy_quantity ~ s(log_n_orders), data = resampled_data)
    predict(gam_model, newdata = data, type = "response")
}

# set resampling number and enable parallel processing
set.seed(123)
boot_results <- boot(
    data = user_activity,
    statistic = bootstrap_gam,
    R = 1000,
    parallel = "multicore",
    ncpus = detectCores() - 1
)

# calculate confidence intervals
predicted_values <- apply(boot_results$t, 2, function(x) {
    c(
        mean = mean(x),
        lower = quantile(x, 0.025),
        upper = quantile(x, 0.975)
    )
})

# create a data frame with the confidence intervals
confidence_intervals <- data.frame(
    log_n_orders = user_activity$log_n_orders,
    predicted = predicted_values["mean", ],
    lower = predicted_values["lower.2.5%", ],
    upper = predicted_values["upper.97.5%", ]
)

# plot the GAM model with confidence intervals
ggplot() +
    geom_point(data = user_activity, aes(x = log_n_orders, y = log_total_buy_quantity), alpha = 0.5) +
    geom_line(data = confidence_intervals, aes(x = log_n_orders, y = predicted), color = "blue") +
    geom_ribbon(data = confidence_intervals, aes(x = log_n_orders, ymin = lower, ymax = upper), alpha = 0.2) +
    labs(
        title = "GAM: Log(Number of Orders) vs Log(Total Buy Quantity) with Bootstrap Confidence Intervals",
        x = "Log(Number of Orders)",
        y = "Log(Total Buy Quantity"
    )
