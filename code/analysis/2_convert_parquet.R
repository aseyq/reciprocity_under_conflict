library(dplyr)
library(ggplot2)
library(here)
library(arrow)

data_dir <- file.path(here(), "..", "..","output","combineddata")
# Load data

df_raw_combined <- read.csv("../../output/combineddata/combined_data.csv")

glimpse(df_raw_combined)

write_parquet(df_raw_combined, "../../output/combineddata/combined.parquet")
