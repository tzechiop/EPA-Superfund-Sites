library(sp)
library(maptools)
library(rgdal)
library(raster)
library(rgeos)
library(rgrass7)
gpclibPermit()
library(reshape2)
library(dplyr)
library(plyr)

#####-----------------------------------------------------------------------------------------------------
setwd("U:/")
fp <- file.path(".", "Passaic_Files", "GIS", "GRASS_EXPORT")
ns <- readOGR(paste(file.path(fp), "navchnl_and_shoal", sep= "/"), "navchnl_and_shoal", stringsAsFactors = F)
fp <- file.path("S:/", "Projects", "passaic", "Data", "Model", "SedTran_RevisedBathy")
alt4 <- readOGR(paste(file.path(fp)), "updated_model_grid_to_send", stringsAsFactors = F)
alt4 <- alt4[which(alt4@data$Alt4_Jul15 == "Yes"), ]
alt4.trans = spTransform(alt4, CRS("+init=ESRI:102711"))

ns83 <- ns[ns@data$RvrMile_st <= 8, ]
ns83.trans = spTransform(ns83, CRS("+init=ESRI:102711"))

# ##### Read in 2378TCDD surface sediment data
# setwd("U:/")
# fp <- file.path(".", "Passaic_Files", "Data")
# dat <- read.csv(paste(file.path(fp, "Dioxin2378_Surf_6in_95_13_NO_RM10_9.csv"), sep= ""), sep = ",",
#                 stringsAsFactors = F, header = T)
# dat_spdf <- SpatialPointsDataFrame(cbind(dat$Easting, dat$Northing),
#                                    data = dat, proj4string = CRS("+init=EPSG:3424"))
# dat_spdf83 <- dat_spdf[dat_spdf@data$River_Mile <= 8.3, ]
# dat_2378tcdd <- dat_spdf83[dat_spdf83@data$CAS_  %in% c("1746-01-6"), ]
# test <- data.frame("ID" = dat_2378tcdd@data$Location_I, "conc" = dat_2378tcdd@data$Concentrat)
# test1 <- data.frame("ID" = sed_2378tcdd@data$Location.ID, "conc" = as.numeric(sed_2378tcdd@data$Final.Concentration))

setwd("U:/")
fp <- file.path(".", "Passaic_Files", "Data", "Sediment_Data")
sed <- read.csv(paste(file.path(fp, "1995-2013partial SurfSed Data.csv"), sep= ""), sep = ",",
                stringsAsFactors = F, header = T)
sed$Final.Concentration[sed$detect_flag == "N"] <- NA
sed_spdf <- SpatialPointsDataFrame(cbind(sed$Easting, sed$Northing),
                                   data = sed, proj4string = CRS("+init=EPSG:3424"))
sed_spdf83 <- sed_spdf[sed_spdf@data$River.Mile <= 8.3, ]
sed_spdf83.trans = spTransform(sed_spdf83, CRS("+init=ESRI:102711"))
sed_spdf83_pre08.trans = sed_spdf83.trans[sed_spdf83.trans@data$Year < 2008, ]
sed_spdf83_pst08.trans = sed_spdf83.trans[sed_spdf83.trans@data$Year >= 2008, ]

sed_2378tcdd <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("1746-01-6"), ]
sed_44dde <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("72-55-9"), ]
sed_tpcb <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("Total PCB"), ]
sed_hg <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("7439-97-6"), ]
sed_cu <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("7440-50-8"), ]
sed_pb <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("7439-92-1"), ]
sed_chd <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("Total Chlordane"), ]
sed_hmw <- sed_spdf83.trans[sed_spdf83.trans$CAS. %in% c("HMW PAH"), ]

sed_2378tcdd_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("1746-01-6"), ]
sed_44dde_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("72-55-9"), ]
sed_tpcb_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("Total PCB"), ]
sed_hg_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("7439-97-6"), ]
sed_cu_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("7440-50-8"), ]
sed_pb_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("7439-92-1"), ]
sed_chd_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("Total Chlordane"), ]
sed_hmw_pre08 <- sed_spdf83_pre08.trans[sed_spdf83_pre08.trans$CAS. %in% c("HMW PAH"), ]

sed_2378tcdd_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("1746-01-6"), ]
sed_44dde_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("72-55-9"), ]
sed_tpcb_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("Total PCB"), ]
sed_hg_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("7439-97-6"), ]
sed_cu_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("7440-50-8"), ]
sed_pb_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("7439-92-1"), ]
sed_chd_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("Total Chlordane"), ]
sed_hmw_pst08 <- sed_spdf83_pst08.trans[sed_spdf83_pst08.trans$CAS. %in% c("HMW PAH"), ]

#####-----------------------------------------------------------------------------------------------------
# Simple Average All Years
sed_2378tcdd_over <- over(x = sed_2378tcdd, y = alt4.trans)
sed_2378tcdd_insideAlt4 <- sed_2378tcdd[which(is.na(sed_2378tcdd_over$ID) == F), ]
sed_2378tcdd_outsideAlt4 <- sed_2378tcdd[which(is.na(sed_2378tcdd_over$ID) == T), ]
sed_2378tcdd_all_mean <- mean(sed_2378tcdd@data$Final.Concentration, na.rm = T)
sed_2378tcdd_insideAlt4_mean <- mean(sed_2378tcdd_insideAlt4@data$Final.Concentration, na.rm = T)
sed_2378tcdd_outsideAlt4_mean <- mean(sed_2378tcdd_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_44dde_over <- over(x = sed_44dde, y = alt4.trans)
sed_44dde_insideAlt4 <- sed_44dde[which(is.na(sed_44dde_over$ID) == F), ]
sed_44dde_outsideAlt4 <- sed_44dde[which(is.na(sed_44dde_over$ID) == T), ]
sed_44dde_all_mean <- mean(sed_44dde@data$Final.Concentration, na.rm = T)
sed_44dde_insideAlt4_mean <- mean(sed_44dde_insideAlt4@data$Final.Concentration, na.rm = T)
sed_44dde_outsideAlt4_mean <- mean(sed_44dde_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_tpcb_over <- over(x = sed_tpcb, y = alt4.trans)
sed_tpcb_insideAlt4 <- sed_tpcb[which(is.na(sed_tpcb_over$ID) == F), ]
sed_tpcb_outsideAlt4 <- sed_tpcb[which(is.na(sed_tpcb_over$ID) == T), ]
sed_tpcb_all_mean <- mean(sed_tpcb@data$Final.Concentration, na.rm = T)
sed_tpcb_insideAlt4_mean <- mean(sed_tpcb_insideAlt4@data$Final.Concentration, na.rm = T)
sed_tpcb_outsideAlt4_mean <- mean(sed_tpcb_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_hg_over <- over(x = sed_hg, y = alt4.trans)
sed_hg_insideAlt4 <- sed_hg[which(is.na(sed_hg_over$ID) == F), ]
sed_hg_outsideAlt4 <- sed_hg[which(is.na(sed_hg_over$ID) == T), ]
sed_hg_all_mean <- mean(sed_hg@data$Final.Concentration, na.rm = T)
sed_hg_insideAlt4_mean <- mean(sed_hg_insideAlt4@data$Final.Concentration, na.rm = T)
sed_hg_outsideAlt4_mean <- mean(sed_hg_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_cu_over <- over(x = sed_cu, y = alt4.trans)
sed_cu_insideAlt4 <- sed_cu[which(is.na(sed_cu_over$ID) == F), ]
sed_cu_outsideAlt4 <- sed_cu[which(is.na(sed_cu_over$ID) == T), ]
sed_cu_all_mean <- mean(sed_cu@data$Final.Concentration, na.rm = T)
sed_cu_insideAlt4_mean <- mean(sed_cu_insideAlt4@data$Final.Concentration, na.rm = T)
sed_cu_outsideAlt4_mean <- mean(sed_cu_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_pb_over <- over(x = sed_pb, y = alt4.trans)
sed_pb_insideAlt4 <- sed_pb[which(is.na(sed_pb_over$ID) == F), ]
sed_pb_outsideAlt4 <- sed_pb[which(is.na(sed_pb_over$ID) == T), ]
sed_pb_all_mean <- mean(sed_pb@data$Final.Concentration, na.rm = T)
sed_pb_insideAlt4_mean <- mean(sed_pb_insideAlt4@data$Final.Concentration, na.rm = T)
sed_pb_outsideAlt4_mean <- mean(sed_pb_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_chd_over <- over(x = sed_chd, y = alt4.trans)
sed_chd_insideAlt4 <- sed_chd[which(is.na(sed_chd_over$ID) == F), ]
sed_chd_outsideAlt4 <- sed_chd[which(is.na(sed_chd_over$ID) == T), ]
sed_chd_all_mean <- mean(sed_chd@data$Final.Concentration, na.rm = T)
sed_chd_insideAlt4_mean <- mean(sed_chd_insideAlt4@data$Final.Concentration, na.rm = T)
sed_chd_outsideAlt4_mean <- mean(sed_chd_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_hmw_over <- over(x = sed_hmw, y = alt4.trans)
sed_hmw_insideAlt4 <- sed_hmw[which(is.na(sed_hmw_over$ID) == F), ]
sed_hmw_outsideAlt4 <- sed_hmw[which(is.na(sed_hmw_over$ID) == T), ]
sed_hmw_all_mean <- mean(sed_hmw@data$Final.Concentration, na.rm = T)
sed_hmw_insideAlt4_mean <- mean(sed_hmw_insideAlt4@data$Final.Concentration, na.rm = T)
sed_hmw_outsideAlt4_mean <- mean(sed_hmw_outsideAlt4@data$Final.Concentration, na.rm = T)

#####-----------------------------------------------------------------------------------------------------
# Simple Average Pre-2008
sed_2378tcdd_pre08_over <- over(x = sed_2378tcdd_pre08, y = alt4.trans)
sed_2378tcdd_pre08_insideAlt4 <- sed_2378tcdd_pre08[which(is.na(sed_2378tcdd_pre08_over$ID) == F), ]
sed_2378tcdd_pre08_outsideAlt4 <- sed_2378tcdd_pre08[which(is.na(sed_2378tcdd_pre08_over$ID) == T), ]
sed_2378tcdd_pre08_all_mean <- mean(sed_2378tcdd_pre08@data$Final.Concentration, na.rm = T)
sed_2378tcdd_pre08_insideAlt4_mean <- mean(sed_2378tcdd_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_2378tcdd_pre08_outsideAlt4_mean <- mean(sed_2378tcdd_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_44dde_pre08_over <- over(x = sed_44dde_pre08, y = alt4.trans)
sed_44dde_pre08_insideAlt4 <- sed_44dde_pre08[which(is.na(sed_44dde_pre08_over$ID) == F), ]
sed_44dde_pre08_outsideAlt4 <- sed_44dde_pre08[which(is.na(sed_44dde_pre08_over$ID) == T), ]
sed_44dde_pre08_all_mean <- mean(sed_44dde_pre08@data$Final.Concentration, na.rm = T)
sed_44dde_pre08_insideAlt4_mean <- mean(sed_44dde_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_44dde_pre08_outsideAlt4_mean <- mean(sed_44dde_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_tpcb_pre08_over <- over(x = sed_tpcb_pre08, y = alt4.trans)
sed_tpcb_pre08_insideAlt4 <- sed_tpcb_pre08[which(is.na(sed_tpcb_pre08_over$ID) == F), ]
sed_tpcb_pre08_outsideAlt4 <- sed_tpcb_pre08[which(is.na(sed_tpcb_pre08_over$ID) == T), ]
sed_tpcb_pre08_all_mean <- mean(sed_tpcb_pre08@data$Final.Concentration, na.rm = T)
sed_tpcb_pre08_insideAlt4_mean <- mean(sed_tpcb_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_tpcb_pre08_outsideAlt4_mean <- mean(sed_tpcb_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_hg_pre08_over <- over(x = sed_hg_pre08, y = alt4.trans)
sed_hg_pre08_insideAlt4 <- sed_hg_pre08[which(is.na(sed_hg_pre08_over$ID) == F), ]
sed_hg_pre08_outsideAlt4 <- sed_hg_pre08[which(is.na(sed_hg_pre08_over$ID) == T), ]
sed_hg_pre08_all_mean <- mean(sed_hg_pre08@data$Final.Concentration, na.rm = T)
sed_hg_pre08_insideAlt4_mean <- mean(sed_hg_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_hg_pre08_outsideAlt4_mean <- mean(sed_hg_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_cu_pre08_over <- over(x = sed_cu_pre08, y = alt4.trans)
sed_cu_pre08_insideAlt4 <- sed_cu_pre08[which(is.na(sed_cu_pre08_over$ID) == F), ]
sed_cu_pre08_outsideAlt4 <- sed_cu_pre08[which(is.na(sed_cu_pre08_over$ID) == T), ]
sed_cu_pre08_all_mean <- mean(sed_cu_pre08@data$Final.Concentration, na.rm = T)
sed_cu_pre08_insideAlt4_mean <- mean(sed_cu_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_cu_pre08_outsideAlt4_mean <- mean(sed_cu_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_pb_pre08_over <- over(x = sed_pb_pre08, y = alt4.trans)
sed_pb_pre08_insideAlt4 <- sed_pb_pre08[which(is.na(sed_pb_pre08_over$ID) == F), ]
sed_pb_pre08_outsideAlt4 <- sed_pb_pre08[which(is.na(sed_pb_pre08_over$ID) == T), ]
sed_pb_pre08_all_mean <- mean(sed_pb_pre08@data$Final.Concentration, na.rm = T)
sed_pb_pre08_insideAlt4_mean <- mean(sed_pb_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_pb_pre08_outsideAlt4_mean <- mean(sed_pb_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_chd_pre08_over <- over(x = sed_chd_pre08, y = alt4.trans)
sed_chd_pre08_insideAlt4 <- sed_chd_pre08[which(is.na(sed_chd_pre08_over$ID) == F), ]
sed_chd_pre08_outsideAlt4 <- sed_chd_pre08[which(is.na(sed_chd_pre08_over$ID) == T), ]
sed_chd_pre08_all_mean <- mean(sed_chd_pre08@data$Final.Concentration, na.rm = T)
sed_chd_pre08_insideAlt4_mean <- mean(sed_chd_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_chd_pre08_outsideAlt4_mean <- mean(sed_chd_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_hmw_pre08_over <- over(x = sed_hmw_pre08, y = alt4.trans)
sed_hmw_pre08_insideAlt4 <- sed_hmw_pre08[which(is.na(sed_hmw_pre08_over$ID) == F), ]
sed_hmw_pre08_outsideAlt4 <- sed_hmw_pre08[which(is.na(sed_hmw_pre08_over$ID) == T), ]
sed_hmw_pre08_all_mean <- mean(sed_hmw_pre08@data$Final.Concentration, na.rm = T)
sed_hmw_pre08_insideAlt4_mean <- mean(sed_hmw_pre08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_hmw_pre08_outsideAlt4_mean <- mean(sed_hmw_pre08_outsideAlt4@data$Final.Concentration, na.rm = T)

#####-----------------------------------------------------------------------------------------------------
# Simple Average Post-2008
sed_2378tcdd_pst08_over <- over(x = sed_2378tcdd_pst08, y = alt4.trans)
sed_2378tcdd_pst08_insideAlt4 <- sed_2378tcdd_pst08[which(is.na(sed_2378tcdd_pst08_over$ID) == F), ]
sed_2378tcdd_pst08_outsideAlt4 <- sed_2378tcdd_pst08[which(is.na(sed_2378tcdd_pst08_over$ID) == T), ]
sed_2378tcdd_pst08_all_mean <- mean(sed_2378tcdd_pst08@data$Final.Concentration, na.rm = T)
sed_2378tcdd_pst08_insideAlt4_mean <- mean(sed_2378tcdd_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_2378tcdd_pst08_outsideAlt4_mean <- mean(sed_2378tcdd_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_44dde_pst08_over <- over(x = sed_44dde_pst08, y = alt4.trans)
sed_44dde_pst08_insideAlt4 <- sed_44dde_pst08[which(is.na(sed_44dde_pst08_over$ID) == F), ]
sed_44dde_pst08_outsideAlt4 <- sed_44dde_pst08[which(is.na(sed_44dde_pst08_over$ID) == T), ]
sed_44dde_pst08_all_mean <- mean(sed_44dde_pst08@data$Final.Concentration, na.rm = T)
sed_44dde_pst08_insideAlt4_mean <- mean(sed_44dde_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_44dde_pst08_outsideAlt4_mean <- mean(sed_44dde_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_tpcb_pst08_over <- over(x = sed_tpcb_pst08, y = alt4.trans)
sed_tpcb_pst08_insideAlt4 <- sed_tpcb_pst08[which(is.na(sed_tpcb_pst08_over$ID) == F), ]
sed_tpcb_pst08_outsideAlt4 <- sed_tpcb_pst08[which(is.na(sed_tpcb_pst08_over$ID) == T), ]
sed_tpcb_pst08_all_mean <- mean(sed_tpcb_pst08@data$Final.Concentration, na.rm = T)
sed_tpcb_pst08_insideAlt4_mean <- mean(sed_tpcb_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_tpcb_pst08_outsideAlt4_mean <- mean(sed_tpcb_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_hg_pst08_over <- over(x = sed_hg_pst08, y = alt4.trans)
sed_hg_pst08_insideAlt4 <- sed_hg_pst08[which(is.na(sed_hg_pst08_over$ID) == F), ]
sed_hg_pst08_outsideAlt4 <- sed_hg_pst08[which(is.na(sed_hg_pst08_over$ID) == T), ]
sed_hg_pst08_all_mean <- mean(sed_hg_pst08@data$Final.Concentration, na.rm = T)
sed_hg_pst08_insideAlt4_mean <- mean(sed_hg_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_hg_pst08_outsideAlt4_mean <- mean(sed_hg_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_cu_pst08_over <- over(x = sed_cu_pst08, y = alt4.trans)
sed_cu_pst08_insideAlt4 <- sed_cu_pst08[which(is.na(sed_cu_pst08_over$ID) == F), ]
sed_cu_pst08_outsideAlt4 <- sed_cu_pst08[which(is.na(sed_cu_pst08_over$ID) == T), ]
sed_cu_pst08_all_mean <- mean(sed_cu_pst08@data$Final.Concentration, na.rm = T)
sed_cu_pst08_insideAlt4_mean <- mean(sed_cu_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_cu_pst08_outsideAlt4_mean <- mean(sed_cu_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_pb_pst08_over <- over(x = sed_pb_pst08, y = alt4.trans)
sed_pb_pst08_insideAlt4 <- sed_pb_pst08[which(is.na(sed_pb_pst08_over$ID) == F), ]
sed_pb_pst08_outsideAlt4 <- sed_pb_pst08[which(is.na(sed_pb_pst08_over$ID) == T), ]
sed_pb_pst08_all_mean <- mean(sed_pb_pst08@data$Final.Concentration, na.rm = T)
sed_pb_pst08_insideAlt4_mean <- mean(sed_pb_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_pb_pst08_outsideAlt4_mean <- mean(sed_pb_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_chd_pst08_over <- over(x = sed_chd_pst08, y = alt4.trans)
sed_chd_pst08_insideAlt4 <- sed_chd_pst08[which(is.na(sed_chd_pst08_over$ID) == F), ]
sed_chd_pst08_outsideAlt4 <- sed_chd_pst08[which(is.na(sed_chd_pst08_over$ID) == T), ]
sed_chd_pst08_all_mean <- mean(sed_chd_pst08@data$Final.Concentration, na.rm = T)
sed_chd_pst08_insideAlt4_mean <- mean(sed_chd_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_chd_pst08_outsideAlt4_mean <- mean(sed_chd_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

sed_hmw_pst08_over <- over(x = sed_hmw_pst08, y = alt4.trans)
sed_hmw_pst08_insideAlt4 <- sed_hmw_pst08[which(is.na(sed_hmw_pst08_over$ID) == F), ]
sed_hmw_pst08_outsideAlt4 <- sed_hmw_pst08[which(is.na(sed_hmw_pst08_over$ID) == T), ]
sed_hmw_pst08_all_mean <- mean(sed_hmw_pst08@data$Final.Concentration, na.rm = T)
sed_hmw_pst08_insideAlt4_mean <- mean(sed_hmw_pst08_insideAlt4@data$Final.Concentration, na.rm = T)
sed_hmw_pst08_outsideAlt4_mean <- mean(sed_hmw_pst08_outsideAlt4@data$Final.Concentration, na.rm = T)

# #####-----------------------------------------------------------------------------------------------------
# ##### Cell Decluster Average over all years
fp <- file.path("U:", "Passaic_Files", "R_code", "functions")
source(paste(fp, "Point_CellDeclustering_v2.R", sep="/"))
cellSize <- seq(1, 500, 1)
sed_2378tcdd_all_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd, "Final.Concentration")
sed_2378tcdd_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_insideAlt4, "Final.Concentration")
sed_2378tcdd_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_outsideAlt4, "Final.Concentration")

sed_44dde_all_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde, "Final.Concentration")
sed_44dde_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_insideAlt4, "Final.Concentration")
sed_44dde_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_outsideAlt4, "Final.Concentration")

sed_tpcb_all_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb, "Final.Concentration")
sed_tpcb_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_insideAlt4, "Final.Concentration")
sed_tpcb_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_outsideAlt4, "Final.Concentration")

sed_hg_all_CD <- Point_CellDeclustering_v2(cellSize, sed_hg, "Final.Concentration")
sed_hg_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_insideAlt4, "Final.Concentration")
sed_hg_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_outsideAlt4, "Final.Concentration")

sed_cu_all_CD <- Point_CellDeclustering_v2(cellSize, sed_cu, "Final.Concentration")
sed_cu_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_insideAlt4, "Final.Concentration")
sed_cu_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_outsideAlt4, "Final.Concentration")

sed_pb_all_CD <- Point_CellDeclustering_v2(cellSize, sed_pb, "Final.Concentration")
sed_pb_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_insideAlt4, "Final.Concentration")
sed_pb_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_outsideAlt4, "Final.Concentration")

sed_chd_all_CD <- Point_CellDeclustering_v2(cellSize, sed_chd, "Final.Concentration")
sed_chd_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_insideAlt4, "Final.Concentration")
sed_chd_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_outsideAlt4, "Final.Concentration")

sed_hmw_all_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw, "Final.Concentration")
sed_hmw_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_insideAlt4, "Final.Concentration")
sed_hmw_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_outsideAlt4, "Final.Concentration")

min(sed_2378tcdd_all_CD[[1]])
min(sed_2378tcdd_insideAlt4_CD[[1]])
min(sed_2378tcdd_outsideAlt4_CD[[1]])

min(sed_44dde_all_CD[[1]])
min(sed_44dde_insideAlt4_CD[[1]])
min(sed_44dde_outsideAlt4_CD[[1]])

min(sed_tpcb_all_CD[[1]])
min(sed_tpcb_insideAlt4_CD[[1]])
min(sed_tpcb_outsideAlt4_CD[[1]])

min(sed_hg_all_CD[[1]])
min(sed_hg_insideAlt4_CD[[1]])
min(sed_hg_outsideAlt4_CD[[1]])

min(sed_cu_all_CD[[1]])
min(sed_cu_insideAlt4_CD[[1]])
min(sed_cu_outsideAlt4_CD[[1]])

min(sed_pb_all_CD[[1]])
min(sed_pb_insideAlt4_CD[[1]])
min(sed_pb_outsideAlt4_CD[[1]])

min(sed_chd_all_CD[[1]])
min(sed_chd_insideAlt4_CD[[1]])
min(sed_chd_outsideAlt4_CD[[1]])

min(sed_hmw_all_CD[[1]])
min(sed_hmw_insideAlt4_CD[[1]])
min(sed_hmw_outsideAlt4_CD[[1]])



setwd("U:/")
fp <- file.path(".", "Passaic_Files", "Data")
write.csv(out2378TCDD$MinMean_Wts,
          paste(fp, "Cell_Declustering_RM0_to_18_MinMeanWts.csv", sep="/"), row.names = F)
plot(1:nrow(sed_hg_outsideAlt4_CD[[1]]), sed_hg_outsideAlt4_CD[[1]], xlab = "Cell Dimension (length of side, ft)",
     ylab = "2378TCDD (pg/g)")

# #####-----------------------------------------------------------------------------------------------------
# ##### Cell Decluster Average over pre-2008 data
fp <- file.path("U:", "Passaic_Files", "R_code", "functions")
source(paste(fp, "Point_CellDeclustering_v2.R", sep="/"))
cellSize <- seq(1, 500, 1)
sed_2378tcdd_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_pre08, "Final.Concentration")
sed_2378tcdd_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_pre08_insideAlt4, "Final.Concentration")
sed_2378tcdd_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_pre08_outsideAlt4, "Final.Concentration")

sed_44dde_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_pre08, "Final.Concentration")
sed_44dde_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_pre08_insideAlt4, "Final.Concentration")
sed_44dde_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_pre08_outsideAlt4, "Final.Concentration")

sed_tpcb_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_pre08, "Final.Concentration")
sed_tpcb_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_pre08_insideAlt4, "Final.Concentration")
sed_tpcb_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_pre08_outsideAlt4, "Final.Concentration")

sed_hg_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_pre08, "Final.Concentration")
sed_hg_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_pre08_insideAlt4, "Final.Concentration")
sed_hg_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_pre08_outsideAlt4, "Final.Concentration")

sed_cu_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_pre08, "Final.Concentration")
sed_cu_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_pre08_insideAlt4, "Final.Concentration")
sed_cu_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_pre08_outsideAlt4, "Final.Concentration")

sed_pb_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_pre08, "Final.Concentration")
sed_pb_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_pre08_insideAlt4, "Final.Concentration")
sed_pb_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_pre08_outsideAlt4, "Final.Concentration")

sed_chd_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_pre08, "Final.Concentration")
sed_chd_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_pre08_insideAlt4, "Final.Concentration")
sed_chd_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_pre08_outsideAlt4, "Final.Concentration")

sed_hmw_pre08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_pre08, "Final.Concentration")
sed_hmw_pre08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_pre08_insideAlt4, "Final.Concentration")
sed_hmw_pre08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_pre08_outsideAlt4, "Final.Concentration")

min(sed_2378tcdd_pre08_all_CD[[1]])
min(sed_2378tcdd_pre08_insideAlt4_CD[[1]])
min(sed_2378tcdd_pre08_outsideAlt4_CD[[1]])

min(sed_44dde_pre08_all_CD[[1]])
min(sed_44dde_pre08_insideAlt4_CD[[1]])
min(sed_44dde_pre08_outsideAlt4_CD[[1]])

min(sed_tpcb_pre08_all_CD[[1]])
min(sed_tpcb_pre08_insideAlt4_CD[[1]])
min(sed_tpcb_pre08_outsideAlt4_CD[[1]])

min(sed_hg_pre08_all_CD[[1]])
min(sed_hg_pre08_insideAlt4_CD[[1]])
min(sed_hg_pre08_outsideAlt4_CD[[1]])

min(sed_cu_pre08_all_CD[[1]])
min(sed_cu_pre08_insideAlt4_CD[[1]])
min(sed_cu_pre08_outsideAlt4_CD[[1]])

min(sed_pb_pre08_all_CD[[1]])
min(sed_pb_pre08_insideAlt4_CD[[1]])
min(sed_pb_pre08_outsideAlt4_CD[[1]])

min(sed_chd_pre08_all_CD[[1]])
min(sed_chd_pre08_insideAlt4_CD[[1]])
min(sed_chd_pre08_outsideAlt4_CD[[1]])

min(sed_hmw_pre08_all_CD[[1]])
min(sed_hmw_pre08_insideAlt4_CD[[1]])
min(sed_hmw_pre08_outsideAlt4_CD[[1]])
# #####-----------------------------------------------------------------------------------------------------
# ##### Cell Decluster Average over p0st-2008 data
fp <- file.path("U:", "Passaic_Files", "R_code", "functions")
source(paste(fp, "Point_CellDeclustering_v2.R", sep="/"))
cellSize <- seq(1, 500, 1)
sed_2378tcdd_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_pst08, "Final.Concentration")
sed_2378tcdd_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_pst08_insideAlt4, "Final.Concentration")
sed_2378tcdd_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_2378tcdd_pst08_outsideAlt4, "Final.Concentration")

sed_44dde_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_pst08, "Final.Concentration")
sed_44dde_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_pst08_insideAlt4, "Final.Concentration")
sed_44dde_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_44dde_pst08_outsideAlt4, "Final.Concentration")

sed_tpcb_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_pst08, "Final.Concentration")
sed_tpcb_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_pst08_insideAlt4, "Final.Concentration")
sed_tpcb_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_tpcb_pst08_outsideAlt4, "Final.Concentration")

sed_hg_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_pst08, "Final.Concentration")
sed_hg_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_pst08_insideAlt4, "Final.Concentration")
sed_hg_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hg_pst08_outsideAlt4, "Final.Concentration")

sed_cu_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_pst08, "Final.Concentration")
sed_cu_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_pst08_insideAlt4, "Final.Concentration")
sed_cu_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_cu_pst08_outsideAlt4, "Final.Concentration")

sed_pb_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_pst08, "Final.Concentration")
sed_pb_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_pst08_insideAlt4, "Final.Concentration")
sed_pb_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_pb_pst08_outsideAlt4, "Final.Concentration")

sed_chd_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_pst08, "Final.Concentration")
sed_chd_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_pst08_insideAlt4, "Final.Concentration")
sed_chd_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_chd_pst08_outsideAlt4, "Final.Concentration")

sed_hmw_pst08_all_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_pst08, "Final.Concentration")
sed_hmw_pst08_insideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_pst08_insideAlt4, "Final.Concentration")
sed_hmw_pst08_outsideAlt4_CD <- Point_CellDeclustering_v2(cellSize, sed_hmw_pst08_outsideAlt4, "Final.Concentration")

min(sed_2378tcdd_pst08_all_CD[[1]])
min(sed_2378tcdd_pst08_insideAlt4_CD[[1]])
min(sed_2378tcdd_pst08_outsideAlt4_CD[[1]])

min(sed_44dde_pst08_all_CD[[1]])
min(sed_44dde_pst08_insideAlt4_CD[[1]])
min(sed_44dde_pst08_outsideAlt4_CD[[1]])

min(sed_tpcb_pst08_all_CD[[1]])
min(sed_tpcb_pst08_insideAlt4_CD[[1]])
min(sed_tpcb_pst08_outsideAlt4_CD[[1]])

min(sed_hg_pst08_all_CD[[1]])
min(sed_hg_pst08_insideAlt4_CD[[1]])
min(sed_hg_pst08_outsideAlt4_CD[[1]])

min(sed_cu_pst08_all_CD[[1]])
min(sed_cu_pst08_insideAlt4_CD[[1]])
min(sed_cu_pst08_outsideAlt4_CD[[1]])

min(sed_pb_pst08_all_CD[[1]])
min(sed_pb_pst08_insideAlt4_CD[[1]])
min(sed_pb_pst08_outsideAlt4_CD[[1]])

min(sed_chd_pst08_all_CD[[1]])
min(sed_chd_pst08_insideAlt4_CD[[1]])
min(sed_chd_pst08_outsideAlt4_CD[[1]])

min(sed_hmw_pst08_all_CD[[1]])
min(sed_hmw_pst08_insideAlt4_CD[[1]])
min(sed_hmw_pst08_outsideAlt4_CD[[1]])

# #####-----------------------------------------------------------------------------------------------------
