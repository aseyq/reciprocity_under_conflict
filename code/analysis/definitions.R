# DEFINITIONS, NAMES, LABELS, COLORS ===========================================

## all strategy types (they are as columns in the data frame)
types <- c(
           "cooperator",
           "defector",
           "match",
           "mismatch",
           "prob05")

population_structures <- c("attackermaj", "attackermin", "equal", "onlyattacker", "onlydefender", 
"prisoner")

## populations structures in order, this of course excludes prisoner's dilemma
popstr_order  <- c("onlydefender",
                   "attackermin",
                   "equal",
                   "attackermaj",
                   "onlyattacker")


## columnames as "cooperator__mean" etc
colnames_n  <- map_chr(types, paste0,  "__mean")
colnames_payoff  <- map_chr(types, paste0, "_payoff_mean")

# labels
type_labels  <- c(
    "cooperator" = "Cooperator",
    "defector" = "Defector",
    "match" = "Matcher",
    "mismatch" = "Mismatcher",
    "prob05" = "Random"
)

labels_n  <- type_labels
names(labels_n)  <- colnames_n

labels_payoff <- type_labels
names(labels_payoff)  <- colnames_payoff

pop_facet_labels  <- c(
    "onlydefender" = "Rousseauian Only",
    "attackermin" = "Rousseauian Majority",
    "equal" = "Equal Proportion",
    "attackermaj" = "Hobbesian Majority",
    "onlyattacker" = "Hobbesian Only",
    "attacker" = "Hobbesian Type",
    "defender" = "Rousseauian Type",
    "prisoner" = "Prisoners' Dilemma"
)


# colors
violet  <- "#6E2594" # Blue violet
orange  <- "#EEC643" # Orange peel
red  <- "#B80C09" # Cardinal red
green  <- "#00A676" # Russian Green
blue  <- "#222E50" #Blue NCS

color_values  <- c(
    "cooperator" = green,
    "defector" = red,
    "match" = blue,
    "mismatch" = orange,
    "prob05" = violet
)

welfare_colors  <- c(
    "onlydefender" = "#5cc5fa",
    "attackermin" = "#3ba6db",
    "equal" = "#2995CB",
    "attackermaj" = "#065f8c",
    "onlyattacker" = "#000048"
)

welfare_labels  <- c(
    "onlydefender" = "Rousseauian Only",
    "attackermin" = "Rousseauian Majority",
    "equal" = "Equal Proportion",
    "attackermaj" = "Hobbesian Majority",
    "onlyattacker" = "Hobbesian Only"
)

evolution_colors <- c(welfare_colors[1:4], "prisoner" = "#8c0618")


colors_n <- color_values
names(colors_n) <- colnames_n

colors_payoff <- color_values
names(colors_payoff)  <- colnames_payoff

popstr_order  <- c("onlydefender",
                   "attackermin",
                   "equal",
                   "attackermaj",
                   "onlyattacker")


## theme

theme_paper  <- theme_bw() +
    theme(strip.background = element_rect(fill = NA)) +
    theme(legend.position = "bottom") +
    theme(panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())
