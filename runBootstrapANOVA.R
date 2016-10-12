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
dat <- dat[is.na(dat$TOC.pct) == F,]
dat <- dat[is.na(dat$Al.pct) == F,]

boot.anova(formula = "TPAH16 ~ Al.pct", data = rawDat,
           reps = 1000, dec = 2)

boot.anova(formula = "TPAH16 ~ TOC.pct", data = rawDat,
           reps = 1000, dec = 2)