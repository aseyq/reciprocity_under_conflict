library(dplyr)
library(ggplot2)
library(here)
library(arrow)

data_dir <- file.path(here(), "data","combined")
# Load data

df_raw_combined <- read.csv("data/combined/ad_combined_2022-03-13.csv")

glimpse(df_raw_combined)

write_parquet(df_raw_combined, "data/combined_parquet/combined.parquet")
