library(readr)
library(dplyr)
library(ggplot2)
library(httpgd)
library(mgcv)
library(boot)
library(parallel)


setwd("/Users/fitz/Coding/immutable_x/src/immutable/analysis")


orders <- read_csv("orders.csv")

orders_filtered <- orders %>%
    filter(buy_type == "ETH")

user_activity <- orders_filtered %>%
    group_by(user) %>%
    summarise(
        n_orders = n(),
        total_buy_quantity = sum(buy_quantity, na.rm = TRUE)
    ) %>%
    mutate(
        log_total_buy_quantity = log(total_buy_quantity + 1), # Log-transform response
        log_n_orders = log(n_orders + 1) # Log-transform predictor
    )

gam_model <- gam(log_total_buy_quantity ~ s(log_n_orders), data = user_activity)

summary(gam_model)

par(mfrow = c(2, 2))
gam.check(gam_model)
par(mfrow = c(1, 1))

plot(gam_model, pages = 1, shade = TRUE, rug = TRUE)

ggplot(user_activity, aes(x = log_n_orders, y = log_total_buy_quantity)) +
    geom_point(alpha = 0.5) +
    stat_smooth(method = "gam", formula = y ~ s(x), col = "blue") +
    labs(
        title = "GAM: Log(Number of Orders) vs Log(Total Buy Quantity)",
        x = "Log(Number of Orders)",
        y = "Log(Total Buy Quantity)"
    )



bootstrap_gam <- function(data, indices) {
    resampled_data <- data[indices, ]
    gam_model <- gam(log_total_buy_quantity ~ s(log_n_orders), data = resampled_data)
    predict(gam_model, newdata = data, type = "response")
}

set.seed(123)
boot_results <- boot(
    data = user_activity,
    statistic = bootstrap_gam,
    R = 1000,
    parallel = "multicore",
    ncpus = detectCores() - 1
)

predicted_values <- apply(boot_results$t, 2, function(x) {
    c(
        mean = mean(x),
        lower = quantile(x, 0.025),
        upper = quantile(x, 0.975)
    )
})

confidence_intervals <- data.frame(
    log_n_orders = user_activity$log_n_orders,
    predicted = predicted_values["mean", ],
    lower = predicted_values["lower.2.5%", ],
    upper = predicted_values["upper.97.5%", ]
)

ggplot() +
    geom_point(data = user_activity, aes(x = log_n_orders, y = log_total_buy_quantity), alpha = 0.5) +
    geom_line(data = confidence_intervals, aes(x = log_n_orders, y = predicted), color = "blue") +
    geom_ribbon(data = confidence_intervals, aes(x = log_n_orders, ymin = lower, ymax = upper), alpha = 0.2) +
    labs(
        title = "GAM: Log(Number of Orders) vs Log(Total Buy Quantity) with Bootstrap Confidence Intervals",
        x = "Log(Number of Orders)",
        y = "Log(Total Buy Quantity"
    )
