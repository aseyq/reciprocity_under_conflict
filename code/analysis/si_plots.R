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

df_long <- read_parquet("data/longdata_parquet/df_long.parquet", as_data_frame = TRUE)

glimpse(df_long)


glimpse(df_long) # take a look at the data

# all possible combinations of parameters
df_long  %>%
    distinct(moran_r,base_fit,mutation_rate, mistake_rate)

default_parameters <- c(
    'totalsize'= 240,
    'base_fit' = 0.01,
    'mutation_rate' = 0.001,
    'mistake_rate' = 0.005,
    'moran_r' = 0.5)

## mistake 0.05
df_long  %>%
    filter(popstr != "prisoner")  %>%
    filter(
        totalsize == default_parameters['totalsize'],
        base_fit == default_parameters['base_fit'],
        mutation_rate == default_parameters['mutation_rate'],
        #mistake_rate == default_parameters['mistake_rate'],
        mistake_rate == 0.05,
        moran_r == default_parameters['moran_r']
    )   %>%
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
    scale_x_continuous(expand=c(0,0), breaks=c(0.6, 0.7, 0.8,0.9, 0.99)) +
    scale_y_continuous(expand=c(0,0),sec.axis = sec_axis(~ . * 1, name = "")) +
    scale_fill_manual(values = color_values,
                        labels = type_labels,
                        name = "",
                        ) +
    coord_fixed(ratio = 0.35) +
    labs(
        x = "Continuation probability",
        y = "Relative Frequency",
        color = "",
    ) +
    theme_paper +
        theme(panel.spacing = unit(1.3, "lines"))

ggsave(filename="plots/SI_success_mistake0_05.png", width=9, height=4)

###
df_long  %>%
    distinct(moran_r,base_fit,mutation_rate, mistake_rate)


### mutation rate 0.01
df_long  %>%
    filter(popstr != "prisoner")  %>%
    filter(
        totalsize == default_parameters['totalsize'],
        base_fit == default_parameters['base_fit'],
        mutation_rate == 0.01,
        mistake_rate == default_parameters['mistake_rate'],
        moran_r == default_parameters['moran_r']
    )   %>%
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
    scale_x_continuous(expand=c(0,0), breaks=c(0.6, 0.7, 0.8,0.9, 0.99)) +
    scale_y_continuous(expand=c(0,0),sec.axis = sec_axis(~ . * 1, name = "")) +
    scale_fill_manual(values = color_values,
                        labels = type_labels,
                        name = "",
                        ) +
    coord_fixed(ratio = 0.35) +
    labs(
        x = "Continuation probability",
        y = "Relative Frequency",
        color = "",
    ) +
    theme_paper +
        theme(panel.spacing = unit(1.3, "lines"))

ggsave(filename="plots/SI_success_mutation0_01.png", width=9, height=4)


### group size
df_long  %>%
    filter(popstr != "prisoner")  %>%
    filter(
        totalsize == 60,
        base_fit == default_parameters['base_fit'],
        mutation_rate == default_parameters['mutation_rate'],
        mistake_rate == default_parameters['mistake_rate'],
        moran_r == default_parameters['moran_r']
    )   %>%
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
    scale_x_continuous(expand=c(0,0), breaks=c(0.6, 0.7, 0.8,0.9, 0.99)) +
    scale_y_continuous(expand=c(0,0),sec.axis = sec_axis(~ . * 1, name = "")) +
    scale_fill_manual(values = color_values,
                        labels = type_labels,
                        name = "",
                        ) +
    coord_fixed(ratio = 0.35) +
    labs(
        x = "Continuation probability",
        y = "Relative Frequency",
        color = "",
    ) +
    theme_paper +
        theme(panel.spacing = unit(1.3, "lines"))

ggsave(filename="plots/SI_success_size60.png", width=9, height=4)



## figure 5
df_long  %>% 
    #filter(mistake_rate != default_parameters['mistake_rate'])  %>% 
    #filter(mutation_rate != default_parameters['mutation_rate']) %>% 
    filter(
    base_fit == default_parameters['base_fit'],
    #mutation_rate == default_parameters['mutation_rate'],
    #mistake_rate == default_parameters['mistake_rate'],
    moran_r == default_parameters['moran_r'])  %>% 
    filter(popstr != "onlyattacker")  %>%
    filter(type == "match")  %>% 
    mutate(rel_mean = mean / size, rel_std = std / size)  %>% 
    filter(population %in% c("defender", "prisoner"))  %>%
    group_by(mistake_rate, mutation_rate, prob_rep, totalsize, popstr)  %>% 
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
    facet_grid(mistake_rate + mutation_rate ~ totalsize,  labeller = label_context) +
    theme_paper +
    labs(
        x = "Continuation probability",
        y = "Relative Frequency",
        color = "",
    ) 

ggsave("plots/SI_matcher.png", height= 10, width = 10)


glimpse(df_long)

df_long  %>% 
    filter(
        population != "prisoner",
        base_fit == default_parameters['base_fit'],
        mutation_rate == default_parameters['mutation_rate'],
        mistake_rate == default_parameters['mistake_rate'],
        moran_r == default_parameters['moran_r'],
        totalsize == 240,
        prob_rep == 0.80,
        )   %>%
        ggplot (aes(y=mean, x=generation, color=type)) +
        geom_line(size=1.5) +
        geom_ribbon(aes(ymin=mean-std, ymax=(mean+std),fill=type), alpha=0.1, color=NA) +
        scale_color_manual(values=color_values, labels=type_labels, name="") +
        scale_fill_manual(values=color_values, labels=type_labels, name="") +
        facet_grid(
        popstr ~ population,
        labeller = labeller(.rows = pop_facet_labels, .cols = pop_facet_labels)
    )  +
        theme_bw()

ggsave("plots/SI_generation_240_prob_rep0_8.png")

