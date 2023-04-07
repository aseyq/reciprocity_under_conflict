library(dplyr)
library(ggplot2)
library(here)
library(arrow)
library(purrr)
library(forcats)
library(patchwork)

print(here()) # here should work most of the time to find your project root, 
       # but if not, you can set the path manually below

setwd(here())
source('code/analysis/definitions.R')

# Parameters for the main manuscript
default_parameters <- c(
    'totalsize'= 240,
    'base_fit' = 0.01, 
    'mutation_rate' = 0.001, 
    'mistake_rate' = 0.005,
    'moran_r' = 0.5)

df_long <- read_parquet("data/longdata_parquet/df_long.parquet", as_data_frame = TRUE)

glimpse(df_long) # take a look at the data

# all possible combinations of parameters
df_long  %>% 
    distinct(totalsize, moran_r,base_fit,mutation_rate, mistake_rate)



df_default <- df_long %>% 
    # filter for default parameters
    filter(totalsize == default_parameters['totalsize'],
           base_fit == default_parameters['base_fit'],
           mutation_rate == default_parameters['mutation_rate'],
           mistake_rate == default_parameters['mistake_rate'],
           moran_r == default_parameters['moran_r'])


# df_default is our main data frame for the main manuscript

# Figure 3 - The relative success of strategies in a cooperative vs competitive environment ===============

figure3 <- df_default  %>%
    filter(popstr %in% c("onlyattacker", "onlydefender"))      %>% 
    mutate(rel_mean = mean / size)  %>%
    group_by(
        popstr,
        prob_rep,
        type,
        population
    )  %>%
    summarize(mean = mean(rel_mean))  %>% 
    ggplot(aes(
        y = mean,
        x = prob_rep,
        fill=type,
    )) +
    geom_area() +
    facet_grid(
        . ~ popstr,
        labeller = labeller(.rows = pop_facet_labels, .cols = pop_facet_labels)
    )  +
    scale_x_continuous(expand=c(0,0), breaks=unique(df_long$prob_rep)) +
    scale_y_continuous(expand=c(0,0),sec.axis = sec_axis(~ . * 1, name = "")) +
    scale_fill_manual(values = color_values,
                        labels = type_labels, 
                        name = "",
                        ) +
    coord_fixed(ratio = 0.5) +
    labs(
        x = "Continuation probability",
        y = "Relative Frequency",
        color = "",
    ) +
    theme_paper +
    theme(
    panel.spacing = unit(2, "lines"),
    ) 

figure3

ggsave(filename="plots/figure3.png", plot=figure3, width = 8, height = 5, units = "in", dpi = 300)

## Figure 4 - The relative success of strategies in a mixed populations =============================
figure4 <- df_default  %>%
    filter(popstr %in% c("attackermaj", "equal", "attackermin")) %>% 
    mutate(rel_mean = mean / size)  %>%
    group_by(
        popstr,
        prob_rep,
        type,
        population
    )  %>%
    summarize(mean = mean(rel_mean))  %>% 
    ggplot(aes(
        y = mean,
        x = prob_rep,
        fill=type,
    )) +
    geom_area() +
    facet_grid(
        population ~ popstr,
        labeller = labeller(.rows = pop_facet_labels, .cols = pop_facet_labels)
    )  +
    scale_x_continuous(expand=c(0,0), breaks=unique(df_long$prob_rep)) +
    scale_y_continuous(expand=c(0,0),sec.axis = sec_axis(~ . * 1, name = "")) +
    scale_fill_manual(values = color_values,
                        labels = type_labels, 
                        name = "",
                        ) +
    coord_fixed(ratio = 0.5) +
    labs(
        x = "Continuation probability",
        y = "Relative Frequency",
        color = "",
    ) +
    theme_paper +   
        theme(panel.spacing = unit(1.5, "lines"))

ggsave(filename="plots/figure4.png", plot=figure4, width = 9.5, height = 8, units = "in", dpi = 300)


# Figure 5 - Reciprocity and the Prisoner’s Dilemma. 

figure5 <- df_long  %>% 
    filter(
    base_fit == default_parameters['base_fit'],
    mutation_rate == default_parameters['mutation_rate'],
    mistake_rate == default_parameters['mistake_rate'],
    moran_r == default_parameters['moran_r'])  %>% 
    filter(popstr != "onlyattacker")  %>%
    filter(type == "match")  %>% 
    mutate(rel_mean = mean / size)  %>% 
    filter(population %in% c("defender", "prisoner"))  %>%
    group_by(prob_rep, totalsize, popstr)  %>% 
    summarize(rel_mean = mean(rel_mean))  %>%
    ggplot(aes(
        x = prob_rep,
        y = rel_mean,
        color= popstr,
    )) +
    scale_color_manual(values=evolution_colors,
 labels = pop_facet_labels, name = "") +
    scale_x_continuous(limits=c(0.6,1), breaks=unique(df_long$prob_rep)) +
    scale_y_continuous(limits=c(0,0.8), breaks=seq(0,1,0.1)) +

    #coord_fixed(ratio = 0.5) +
    geom_point(size=2) +
    geom_line() +
    facet_grid(
        . ~ totalsize,
    ) +
    theme_paper +
    labs(
        x = "Continuation probability",
        y = "Relative Frequency",
        color = "",
    ) 

figure5

ggsave(filename="plots/figure5.png", plot=figure5, width = 9, height = 4.5, units = "in", dpi = 300)


# Figure 6.a Cooperation rates
df_coop <- read_parquet("data/longdata_parquet/df_coop.parquet", as_data_frame = TRUE)



df_heatmap <-  df_coop  %>%
    mutate(popstr = fct_relevel(popstr, popstr_order))  %>%
    #select(c(population:num_def__max,-ends_with("__size")))  %>%
    rename(num_coop = num_coop__mean, num_def = num_def__mean)  %>%
    mutate(p_coop = num_coop / (num_coop + num_def),
           p_def = num_def / (num_coop + num_def))  %>%
    group_by(
        totalsize,
        base_fit,
        mutation_rate,
        mistake_rate,
        moran_r,
        popstr,
        prob_rep,
        population
    )  %>%
    summarize(p_coop = mean(p_coop))  %>%
    mutate(blockwidth = if_else(prob_rep == 0.99, 0.03, 0.05))  %>%
    mutate(position = if_else(prob_rep == 0.99, 1, prob_rep))

df_heatmap <- df_heatmap  %>% 
    filter(population != "prisoner")  %>%
    ## default parameters
    filter(
        totalsize == default_parameters['totalsize'],
        base_fit == default_parameters['base_fit'],
        mutation_rate == default_parameters['mutation_rate'],
        mistake_rate == default_parameters['mistake_rate'],
        moran_r == default_parameters['moran_r']
    )  


heatmap_breaks <- unique(df_heatmap$prob_rep)

figure6a <- df_heatmap  %>% 
    filter(population != "prisoner")  %>%
    ggplot(aes(
        x = as.factor(prob_rep),
        y = popstr,
        fill = p_coop
    )) +
    geom_tile(width = 1)+
    geom_text(
        aes(label = round(p_coop, 2)),
        alpha = 0.9,
        size = 3.5,
        color="white",
    )  +
    facet_grid(
        population ~ .,
        labeller = as_labeller(pop_facet_labels),
        scales = "free_y",
    ) +
    scale_y_discrete("", labels = pop_facet_labels) +
    scale_x_discrete("Continuation prob.", breaks =
                                                heatmap_breaks) +
    scale_fill_viridis_c(
        "Cooperation rate",
        limits = c(0.25, 0.95)) +
    theme(
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank()
    ) +
        theme_paper +
        guides(fill = "none")

ggsave(filename="plots/figure6a.png", plot=figure6a, width = 5, height = 6, units = "in", dpi = 300)



# Figure 6.b Welfare
df_aggregate_payoffs <- read_parquet("data/longdata_parquet/df_aggregate_payoffs.parquet")

figure6b <- df_aggregate_payoffs  %>% 
    filter(
        totalsize == default_parameters['totalsize'],
        base_fit == default_parameters['base_fit'],
        mutation_rate == default_parameters['mutation_rate'],
        mistake_rate == default_parameters['mistake_rate'],
        moran_r == default_parameters['moran_r']
    )   %>% 
    filter(population != "prisoner")  %>%
    group_by(popstr, prob_rep, population, size, totalsize)  %>% 
    summarize(avg_payoff = mean(avg_payoff_per_interaction)) %>%
    ## we gotta weight different populations before aggregating them since they have different sizes
    mutate(weighted_avg_payoff = avg_payoff * size / totalsize)  %>% 
    group_by(popstr, prob_rep)  %>% 
    summarise(avg_payoff = sum(weighted_avg_payoff))  %>% 
    ggplot(aes(y=avg_payoff, x=prob_rep, color=popstr)) +
    geom_point(size=2) +
    geom_line() +
    scale_color_manual(values=welfare_colors, labels=welfare_labels) +
    scale_x_continuous(limits=c(0.6,1), breaks=unique(df_long$prob_rep)) +
    scale_y_continuous(limits=c(0,2), breaks=seq(0,2,0.25)) +

    expand_limits(y = 0) +
    theme_paper +
    guides(color=guide_legend(nrow=2, byrow=TRUE)) +
    labs(x="Continuation probability", y="Average payoff per interaction", color="") 

figure6b


ggsave(filename="plots/figure6b.png", plot=figure6b, width = 6, height = 5, units = "in", dpi = 300)


figure6 <- figure6a + figure6b
ggsave("plots/figure6.png", plot=figure6, width = 11, height = 6, units = "in", dpi = 300)
