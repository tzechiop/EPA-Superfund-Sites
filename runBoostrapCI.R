
# function to obtain R-Squared from the data 
medstat <- function(refdata, data, indices) {
  d <- data[indices] # allows boot to select sample 
  stat <- median(d)
  refstat <- median(sample(refdata, length(refdata), replace = TRUE))
  ratio <- stat/refstat
  return(ratio)
} 

# Run BoostrapANOVA.R to initialize function
fp <- 'C:/Users/thasegawa/Documents/68 NYC DEP Papers/06 Scripts'
source(paste(file.path(fp, "BootstrapANOVA.R"), sep= ""))

# Read data
fp <- 'C:/Users/thasegawa/Documents/68 NYC DEP Papers/05 Data/Newtown Creek/Bootstrap_20161004'
rawDat <- read.csv(file.path(fp,
                             'anova.analysis.csv'),
                   stringsAsFactors = F,
                   header = T)

dat <- rawDat[is.na(rawDat$TPAH16) == F, ]

canal_list <- c('Canal - Lower',
                'Canal - Middle',
                'Canal - Upper',
                'NTC Mainstem (No TB)',
                'NTC Tributaries',
                'NTC Turning Basin',
                'East River Ref Area')
studyarea_list <- canal_list[-length(canal_list)]

chem <- 'TPAH16'

# bootstrapping with 1000 replications for each canal
refdata <- dat[dat$Category == 'East River Ref Area',chem]
results <- c()
for (studyarea in studyarea_list) {
  sub <- dat[dat$Category == studyarea,chem]
  results[[studyarea]] <- boot(data=sub, statistic=medstat, 
                               R=1000, refdata = refdata)
}

# get 97.5% confidence interval 
df <- c('Category', 'Normal (low)', 'Normal (high)', 'Basic (low)', 'Basic (high)', 'Percentile (low)', 'Percentile (high)', 'BCa (low)', 'BCa (high)')
for (studyarea in studyarea_list) {
  xyz <- boot.ci(results[[studyarea]], conf = .975, type="all")
  newrow <- c()
  newrow[1] <- studyarea 
  i <- 2
  for (type in c('normal', 'basic', 'percent', 'bca')) {
    conf <- xyz[[type]]
    newrow[i] <- as.numeric(conf[length(conf) - 1])
    i <- i + 1
    newrow[i] <- as.numeric(conf[length(conf)])
    i <- i + 1
  }
  df <- rbind(df, newrow)
}

setwd(fp)
write.table(df, file = "TPAH16RefAreaRatio_BoostrapConfidenceIntervals_R_20161012.csv", sep = ",")

for (studyarea in studyarea_list) {
  ratios <- results[[studyarea]]$t
  write.table(ratios, file = sprintf('TPAH16RefAreaRatio_BootstrapMedians_R_%s_20161012.csv', studyarea), row.names = FALSE, col.names = FALSE)
}