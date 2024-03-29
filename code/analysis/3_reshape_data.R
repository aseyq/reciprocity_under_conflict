library(dplyr)
library(ggplot2)
library(here)
library(arrow)
library(purrr)
library(tidyr)
library(forcats)
library(stringr)

## set working directory to the root of the project
print("Working directory: ")
print(here()) # here should work most of the time to find your project root, 
       # but if not, you can set the path manually below

#setwd(here())

# Load data
#   You can use also the csv files, but the parquet files are faster to load and have a smaller size
df_combined <- read_parquet("../../output/combineddata/combined.parquet", as_data_frame = TRUE)


## DEFINITIONS, NAMES, LABELS, COLORS ===========================================
source('definitions.R')

### RESHAPING DATA ================================================================
df_types  <- df_combined  %>%
    # select parameters and type n reladed vaiables
    select(c(
        population:mistake_rate,
        defector__size,
        defector__std,
        defector__mean,
        defector__min,
        defector__max,
        prob05__size,
        prob05__std,
        prob05__mean,
        prob05__min,
        prob05__max,
        match__size,
        match__std,
        match__mean,
        match__min,
        match__max,
        mismatch__size,
        mismatch__std,
        mismatch__mean,
        mismatch__min,
        mismatch__max,
        cooperator__size,
        cooperator__std,
        cooperator__mean,
        cooperator__min,
        cooperator__max,
        -ends_with("__size")
    )) %>%
    # convert it to long form "typename__max" "typename_min" etc for all types
    pivot_longer(
        cols = c(
          "defector__std",
          "defector__mean",
          "defector__min",
          "defector__max",
          "prob05__std",
          "prob05__mean",
          "prob05__min",
          "prob05__max",
          "match__std",
          "match__mean",
          "match__min",
          "match__max",
          "mismatch__std",
          "mismatch__mean",
          "mismatch__min",
          "mismatch__max",
          "cooperator__std",
          "cooperator__mean",
          "cooperator__min",
          "cooperator__max"
        ),
        names_to = c("type", ".value"),
        names_sep = "__"
    )


df_payoffs  <- df_combined  %>%
    # select parameters and type n reladed vaiablesg()
    select(
        c(
            population:mistake_rate,
            cooperator_payoff__size,
            cooperator_payoff__std,
            cooperator_payoff__mean,
            cooperator_payoff__min,
            cooperator_payoff__max,
            defector_payoff__size,
            defector_payoff__std,
            defector_payoff__mean,
            defector_payoff__min,
            defector_payoff__max,
            match_payoff__size,
            match_payoff__std,
            match_payoff__mean,
            match_payoff__min,
            match_payoff__max,
            mismatch_payoff__size,
            mismatch_payoff__std,
            mismatch_payoff__mean,
            mismatch_payoff__min,
            mismatch_payoff__max,
            prob05_payoff__size,
            prob05_payoff__std,
            prob05_payoff__mean,
            prob05_payoff__min,
            prob05_payoff__max,
            -ends_with("__size")
        )
    )  %>%
    pivot_longer(
        cols = cooperator_payoff__std:prob05_payoff__max,
        names_to = c("type", ".value"),
        names_sep = "__"
    )  


glimpse(df_combined)

df_aggregate_payoffs <- df_combined %>% 
# don't be fooleb by "mean" here, these are the average total payoffs per type
    mutate(total_payoff = cooperator_payoff__mean+ 
               defector_payoff__mean  + 
               prob05_payoff__mean  +
               match_payoff__mean  +
               mismatch_payoff__mean ) %>%
    mutate(avg_payoff = total_payoff / size)  %>% 
    mutate(avg_payoff_per_interaction = avg_payoff * (1- prob_rep))  %>% 
    select(population,
           generation,
           totalsize,
           size,
           num_generations,
           prob_rep,
           moran_r,
           base_fit,
           mutation_rate,
           popstr,
           mistake_rate,
           total_payoff, avg_payoff, avg_payoff_per_interaction)


write_parquet(df_aggregate_payoffs, "../../output/processeddata/df_aggregate_payoffs.parquet")

    

df_long <- df_payoffs  %>%
    mutate(type = str_remove(type, "_payoff"))  %>% 
           rename(payoff_std = std,
           payoff_total = mean,
           payoff_total_min = min,
           payoff_total_max = max)  %>% right_join(df_types,
                                             by = c("population",
                                                    "generation",
                                                    "totalsize",
                                                    "size",
                                                    "num_generations",
                                                    "prob_rep",
                                                    "moran_r",
                                                    "base_fit",
                                                    "mutation_rate",
                                                    "popstr",
                                                    "mistake_rate",
                                                    "type"))  %>%
        mutate(popstr = fct_relevel(popstr, popstr_order))  %>%
    mutate(payoff = payoff_total / mean)

           
rm(df_payoffs)
rm(df_types)

write_parquet(df_long, "../../output/processeddata/df_long.parquet")



df_coop  <- df_combined  %>%
    # select parameters and related variables
    dplyr::select(c(population:mistake_rate,num_coop__mean:num_def__mean))  %>% 
    glimpse()

write_parquet(df_coop, "../../output/processeddata/df_coop.parquet")
