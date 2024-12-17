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

# Fit a linear model (GLM)
glm_model <- lm(log_total_buy_quantity ~ log_n_orders, data = user_activity)

# Fit a GAM model
gam_model <- gam(log_total_buy_quantity ~ s(log_n_orders), data = user_activity)

# Create a new data frame for predictions
prediction_data <- data.frame(
    log_n_orders = seq(min(user_activity$log_n_orders), max(user_activity$log_n_orders), length.out = 100)
)

# Add predictions for GLM and GAM
prediction_data$glm_predictions <- predict(glm_model, newdata = prediction_data)
prediction_data$gam_predictions <- predict(gam_model, newdata = prediction_data)

# Plot actual data and overlay both models
ggplot(user_activity, aes(x = log_n_orders, y = log_total_buy_quantity)) +
    geom_point(alpha = 0.5, color = "blue") + # Scatter plot of the actual data
    geom_line(data = prediction_data, aes(x = log_n_orders, y = glm_predictions), color = "red", size = 1, linetype = "dashed") + # GLM fit
    geom_line(data = prediction_data, aes(x = log_n_orders, y = gam_predictions), color = "green", size = 1) + # GAM fit
    labs(
        title = "GLM vs GAM Comparison: Log(Number of Orders) vs Log(Total Buy Quantity)",
        x = "Log(Number of Orders)",
        y = "Log(Total Buy Quantity)"
    ) +
    annotate("text", x = 3.5, y = 2.5, label = "GLM (Linear) - Red Dashed", color = "red", size = 4, hjust = 0) +
    annotate("text", x = 3.5, y = 2.3, label = "GAM (Smooth) - Green Solid", color = "green", size = 4, hjust = 0) +
    theme_minimal()

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
