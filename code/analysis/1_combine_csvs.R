library(data.table)

# Set the working directory to the folder containing the CSV files
setwd("../../output/simulationdata")


# List all the CSV files in the folder
csv_files <- list.files(pattern = "*.csv")

message("Combininig following files")
print(csv_files)
# Initialize an empty data.table to store the combined data
combined_data <- data.table()

# Loop through each CSV file and read its contents
for (file in csv_files) {
  # Read the CSV file and convert it to a data.table
  data <- fread(file, stringsAsFactors = FALSE)
  
  # Bind the data to the combined_data table
  combined_data <- rbind(combined_data, data)
}

message("writing...")
message("output/combineddata/combineddata.csv")
# Save the combined data to a CSV file
fwrite(combined_data, "../combineddata/combined_data.csv")
