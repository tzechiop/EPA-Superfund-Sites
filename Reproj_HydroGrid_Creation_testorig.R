library(sp)
library(maptools)
library(rgdal)
library(raster)
library(rgeos)
library(rgrass7)
library(chron)
gpclibPermit()
library(gstat)
library(geoR)
library(MASS)
library(automap)
#####---------------------------------------------------------------------------
#####---------------------------------------------------------------------------
###### Read in shapefile of polygons
# Area of Influence of UltraSeep locations
fp <- "C:/Users/thasegawa/Documents/68 NYC DEP Papers/05 Data/Newtown Creek/GC-Density Averaging/Straightened Grid"
aoi <- readOGR(paste(file.path(fp)), "Ultraseep_New_AreaOfInfluence_04082016",
               stringsAsFactors = F)
aoi <- spTransform(aoi, CRS("+init=EPSG:26918"))

# UltraSeep locations
fp <- "C:/Users/thasegawa/Documents/68 NYC DEP Papers/05 Data/Newtown Creek/GC-Density Averaging/Straightened Grid"
us <- readOGR(paste(file.path(fp)), "UltraseepLocs_2014and2016_withUS1centroid",
              stringsAsFactors = F)
us <- spTransform(us, CRS("+init=EPSG:26918"))

#Update us shapefile with true average vert seepage rate
m <- match(us$SampleLoc, aoi$SampleLoc)
us$AvgQ_cmDay <- aoi$AvgQ_cmDay[m]
# us$ModVqCMD <- aoi$ModVqCMD[m]
# us$AvgQ_cmDay[which(us$SampleLoc == "NTC21")] <- 0

# Hydro Grid
fp <- "C:/Users/thasegawa/Documents/68 NYC DEP Papers/05 Data/Newtown Creek/GC-Density Averaging"
grd <- readOGR(paste(file.path(fp)), "NC04", stringsAsFactors = F)
nc_grd <- grd[which(grd@data$NC == 1),]
nc_grd <- spTransform(nc_grd, CRS("+init=EPSG:26918"))

#####---------------------------------------------------------------------------
##### Calculate which Hydro Grid polygon each ultraseep location is in
us_over <- over(SpatialPoints(coordinates(us), CRS("+init=EPSG:26918")), nc_grd)
nc_grd_over <- nc_grd[match(us_over$Id, nc_grd$Id), ]
nc_grd_over$USeepID <- us$SampleLoc
nc_grd_over_corners <- lapply(nc_grd_over@polygons, function(y) 
                              (y@Polygons[[1]]@coords))

#####---------------------------------------------------------------------------
##### Calculate the distance the ultraseep point is from each of the Hydro Grid polygon sides
# North Distance
westDistance <- vector()
for(i in 1:length(nc_grd_over_corners)){
  sl <- SpatialLines(list(Lines(Line(matrix(nc_grd_over_corners[[i]][1:2, ], ncol = 2)), ID="a")),
                     CRS("+init=EPSG:26918"))
  westDistance[i] <- gDistance(us[i,], sl)
}

# South Distance
eastDistance <- vector()
for(i in 1:length(nc_grd_over_corners)){
  sl <- SpatialLines(list(Lines(Line(matrix(nc_grd_over_corners[[i]][3:4, ], ncol = 2)), ID="a")),
                     CRS("+init=EPSG:26918"))
  eastDistance[i] <- gDistance(us[i,], sl)
}

# East Distance
northDistance <- vector()
for(i in 1:length(nc_grd_over_corners)){
  sl <- SpatialLines(list(Lines(Line(matrix(nc_grd_over_corners[[i]][2:3, ], ncol = 2)), ID="a")),
                     CRS("+init=EPSG:26918"))
  northDistance[i] <- gDistance(us[i,], sl)
}

# West Distance
southDistance <- vector()
for(i in 1:length(nc_grd_over_corners)){
  sl <- SpatialLines(list(Lines(Line(matrix(nc_grd_over_corners[[i]][c(4,1), ], ncol = 2)), ID="a")),
                     CRS("+init=EPSG:26918"))
  southDistance[i] <- gDistance(us[i,], sl)
}

#####---------------------------------------------------------------------------
##### Determine the fractional distance from the north and south, and from east and west
dist <- data.frame("northDis" = northDistance, 
                   "southDis" = southDistance, 
                   "eastDis" = eastDistance, 
                   "westDis" = westDistance)
fracDist <- list()
for(i in 1:nrow(dist)){
  fracDist[[i]] <- c(dist$northDis[i]/sum(dist$northDis[i], dist$southDis[i]),
                     dist$southDis[i]/sum(dist$northDis[i], dist$southDis[i]),
                     dist$eastDis[i]/sum(dist$eastDis[i], dist$westDis[i]),
                     dist$westDis[i]/sum(dist$eastDis[i], dist$westDis[i]))
}
fracDist <- do.call("rbind", fracDist)

#####---------------------------------------------------------------------------
##### Reproject Hydro Grid as straighted grid (only for main stem!  No tribs!)
NSbounds <- c(33:39) # N-S width of main stem Hydro Grid
EWbounds <- c(13:115) # E-W length of main stem Hydro Grid
xlen <- 1 # x dimension of straightened grid cell (m)
ylen <- 1 # y dimention of straightened grid cell (m)
 reproj_grd <- nc_grd[which(nc_grd$JJ %in% NSbounds), ] # select only cells in turning basin/main stem
 reproj_grd <- reproj_grd[which(!reproj_grd$II %in% 116:130), ] # select only cells in turning basin/main stem

# Create grid
gt <- GridTopology(c(0.5,0.5), c(1,1), c(length(EWbounds), length(NSbounds))) 
sg <- SpatialGrid(gt, proj4string = CRS("+init=EPSG:26918"))

# convert hydro grid cell coords to "straight" cell coords
reproj_grd$Xgrid <- reproj_grd$II - 13 # Recalibrate zero of X coordinates
reproj_grd$Ygrid <- reproj_grd$JJ - 33 # Recalibrate zero of Y coordinates
nc_grd_over$Xgrid <- nc_grd_over$II - 13 # Recalibrate zero of X coordinates
nc_grd_over$Ygrid <- nc_grd_over$JJ - 33 # Recalibrate zero of Y coordinates

# using hydro grid cell coords to calculate Ultraseep point "straight" coords
# Calculate location of ultraseep points on the recalibrated XY coordinates
nc_grd_over$XgridFrac <- (nc_grd_over$II - 13) + (xlen/1)*fracDist[,4]
nc_grd_over$YgridFrac <- (nc_grd_over$JJ - 33) + (ylen/1)*fracDist[,2]

# create Ultraseep "straightened" points
us_str_points <- SpatialPoints(matrix(c(nc_grd_over@data$XgridFrac, 
                                        nc_grd_over@data$YgridFrac), ncol = 2),
                               CRS("+init=EPSG:26918"))
us_str_points_spdf <- SpatialPointsDataFrame(us_str_points, data = us@data)
us_str_points_spdf$X <- nc_grd_over@data$XgridFrac
us_str_points_spdf$Y <- nc_grd_over@data$YgridFrac
us_str_points_spdfSUB <- subset(us_str_points_spdf, us_str_points_spdf$Y <= 7 & 
                                  us_str_points_spdf$Y >= 0)
us_str_points_spdfSUB <- subset(us_str_points_spdfSUB, us_str_points_spdfSUB$X <= 103 & 
                                  us_str_points_spdfSUB$Y >= 0)
##### Test plot
plot(sg)
points(us_str_points_spdfSUB, col = "red", pch = 20)
points(us_str_points_spdf[which(us_str_points_spdf$SampleLoc == "NTC"), ], 
       col = "black", pch = 20)
test <- SpatialPoints(matrix(c(0.5, 0.5), ncol = 2), CRS("+init=EPSG:26918"))
points(test, col = "blue")

#####---------------------------------------------------------------------------
##### Interpolate vertical seepage onto straightened grid using Inverse Distance Weighting (IDW)
# Specify data frame to use for interpolation
data <- us_str_points_spdfSUB

# Inverse distance weighting
idw_sg <- idw(formula = AvgQ_cmDay~1, locations = data,  newdata = sg) #idp = 2
sg_sgdf <- SpatialGridDataFrame(sg, data = as.data.frame(idw_sg))
sgRaster <- raster(sg_sgdf, layer=1, values=TRUE)

# Test Plot IDW grid
spplot(sg_sgdf["var1.pred"])
plot(us_str_points_spdfSUB$AvgQ_cmDay, extract(sgRaster, us_str_points_spdfSUB),
     ylab = "IDW Vert. Seep. (cm/day)", xlab = "ULTRASeep Vert. Seep. (cm/day)",
     pch = 20, cex = 1.5, ylim = c(0, 5), xlim = c(0, 5))
lines(c(-100, 100), c(-100, 100), lty = 2, lwd = 1)

#####---------------------------------------------------------------------------
# ##### Leave one out cross validation test for IDW. Not used!!!
# # Specify data frame to use for interpolation
# data <- us_str_points_spdfSUB
# 
# LOOCV_Pred <- vector()
# LOOCV_Pred0 <- vector()
# # loop through, removing one point at a time and calculating IDW
# for(i in 1:nrow(data@data)){
#   tmp <- data[-i, ]
#   # Inverse distance weighting
#   idw_sg0 <- idw0(formula = AvgQ_cmDay~1, data = data[-i, ],  newdata = data[i, ])
#   LOOCV_Pred[i] <- idw_sg$var1.pred
#   LOOCV_Pred0[i] <- idw_sg0
# }
# plot(data@data$AvgQ_cmDay, (LOOCV_Pred0), xlab = "ULTRASeep Meas. Vertical Seep. (cm/day)",
#      ylab = "LOOCV prediction (cm/day", pch = 20, cex = 1.5, xlim = c(0, 5), ylim = c(0,5))
# lines(c(-100, 100), c(-100, 100), lty = 2, lwd = 1)

#####---------------------------------------------------------------------------
# Remap IDW onto orginal Hydro Grid
nc_grd@data$AREA <- NA
nc_grd$VqIDW <- NA
nc_grd@data$VqIDW_MGY <- NA

sg_sgdf$II <- (sg_sgdf$s1 - 0.5) + 13 # Recalibrate zero of X coordinates
sg_sgdf$JJ <- (sg_sgdf$s2 - 0.5) + 33 # Recalibrate zero of X coordinates

# remap onto mainstem/turning basin Hydro Grid
reproj_grd$VqIDW <- sapply(1:nrow(reproj_grd), function(x)
  sg_sgdf$var1.pred[which(sg_sgdf$II == reproj_grd@data$II[x] &
                            sg_sgdf$JJ == reproj_grd@data$JJ[x])])

# remap onto entire NTC Hydro Grid
m <- match(reproj_grd$Id, nc_grd$Id)
nc_grd$VqIDW[m] <- reproj_grd$VqIDW

# Calculate vertical seepage in MGY
p <- lapply(nc_grd@polygons , slot , "Polygons")
for(i in 1:length(p)){
  nc_grd@data$AREA[i] <- unlist(lapply(p[[i]], function(x) slot(x, "area")))
  nc_grd$VqIDW_MGY[i] <- nc_grd$VqIDW[i]*365/100*nc_grd@data$AREA[i]*264.172/1e6 
}

#####---------------------------------------------------------------------------
#####---------------------------------------------------------------------------
# Export x,y coordinates for straightened points and modeled and observed seepage
m <- match(us_str_points_spdfSUB$SampleLoc, aoi$SampleLoc)
us_str_points_spdfSUB$AvgQ_cmDay <- aoi$AvgQ_cmDay[m]
# us_str_points_spdfSUB$ModVqCMD <- aoi$ModVqCMD[m]
# us_str_points_spdfSUB$AvgQ_cmDay[which(us_str_points_spdfSUB$SampleLoc == "NTC21")] <- 0.01

sub_out <- us_str_points_spdfSUB@data[c("SampleLoc", "X", "Y", "AvgQ_cmDay")]
fp <- "C:/Users/thasegawa/Documents/68 NYC DEP Papers/05 Data/Newtown Creek/GC-Density Averaging/Straightened Grid/Tables"
write.csv(sub_out, paste(fp, "Straightened_UltraSeep_Coords_and_Vseep.csv", sep="/"),
          row.names = F, quote = F)

# fp <- "C:/Users/thasegawa/Documents/68 NYC DEP Papers/05 Data/Newtown Creek/GC-Density Averaging/Straightened Grid/Tables"
# write.csv(vgm, paste(fp, "Variogram_Data_For_Vseep.csv", sep="/"),
#           row.names = F, quote = F)
# 
# spplot(nc_grd["VseepIDW"])

#####---------------------------------------------------------------------------
#####---------------------------------------------------------------------------
#####---------------------------------------------------------------------------
##### Interpolate vertical seepage onto straightened grid using Ordinary Kriging (OK)
# Specify data frame to use for interpolation
dat <- us_str_points_spdfSUB

# Specify para
cutoff = 90 #max lag distance for variogram
width = cutoff/15 #lag width

# calculate sample variogram
vgm = variogram((AvgQ_cmDay) ~ 1, data = dat,
                cutoff = cutoff, width=width, alpha = c(90),
                tol.hor = 25)

# Calculate model variogram and variogram line
null.vgm <- vgm("Sph") #vgm(var(data$AvgQ_cmDay), "Sph") , nugget=0.2) # initial parameters #range = sqrt(areaSpatialGrid(sg))/4
vgm.fit <- fit.variogram(vgm, model=null.vgm, fit.sills = T, fit.ranges = T)
variogram = autofitVariogram((AvgQ_cmDay) ~ 1, input_data = dat, model = "Sph")
varioLine <- variogramLine(vgm(psill = vgm.fit$psill[2],
                               "Sph", range = vgm.fit$range[2],
                               nugget = vgm.fit$psill[1]), 100, 80)

# Plot semi-variogram  
par(mar = c(4,4,4,4), font=2, font.axis = 2, tck = 0.01)
plot(vgm$dist, vgm$gamma, xlim = c(0, 100), pch = 20, col = "blue", cex  = 2,
     ylim = c(0, 2), ann = F)
mtext(side = 1, text = "Lag Distance (m)", line = 2)
mtext(side = 2, text = "Semi-variance (m2)", line = 2)
lines(varioLine$dist, varioLine$gamma)
legend(x = 0, y = 2, "Model Variogram. Dir: East, tol:25deg", col = "black", lty = 1, bty = "n")

# Krige onto spatialGrid
#kr_sg <- krige(AvgQ_cmDay ~ 1, locations = data, newdata = sg, model=null.vgm)
kr_sg <- gstat(id="VSeepKR", formula = AvgQ_cmDay~1, data=dat,
               model = vgm(psill = (0.1750003), "Sph", range = 8.876058, nugget = 1.0026066))
kr_sgPred <- predict(kr_sg, newdata = sg)
kr_sgdf <- SpatialGridDataFrame(sg, data = as.data.frame(kr_sgPred))
#kr_sgdf <- SpatialGridDataFrame(sg, data = as.data.frame(kr_sg))

# Plot checks
spplot(kr_sgdf["VSeepKR.pred"])
kr_sgRaster <- raster(kr_sgdf, layer="VSeepKR.pred", values=TRUE)
plot(us_str_points_spdfSUB$AvgQ_cmDay, extract(kr_sgRaster, us_str_points_spdfSUB),
     ylab = "OK Vert. Seep. (cm/day)", xlab = "ULTRASeep Vert. Seep. (cm/day)",
     pch = 20, cex = 1.5, ylim = c(0, 5), xlim = c(0, 5))
lines(c(-100, 100), c(-100, 100), lty = 2, lwd = 1)

#####---------------------------------------------------------------------------
##### Leave one out cross validation test for OK
# Specify data frame to use for interpolation
dat <- us_str_points_spdfSUB
cutoff = 90
width = cutoff/15

LOOCV_Pred0 <- vector()
# loop through, removing one point at a time and calculating OK
for(i in 1:nrow(dat@data)){
  tmp <- dat[-i, ]
  
  # calculate sample variogram and model fit
  vgm = variogram((AvgQ_cmDay) ~ 1, data = tmp,
                  cutoff = cutoff, width=width, alpha = c(0),
                  tol.hor = 90)
  null.vgm <- vgm("Sph")
  vgm.fit <- fit.variogram(vgm, model=null.vgm, fit.sills = T, fit.ranges = T)
  
  # Inverse distance weighting
  idw_sg0 <- krige0(formula = AvgQ_cmDay~1, data = tmp,  newdata = data[i, ],
                  model = vgm(psill = vgm.fit$psill[2],
                              "Sph", range = vgm.fit$range[2],
                              nugget = vgm.fit$psill[1]))
  LOOCV_Pred0[i] <- idw_sg0
}
plot(data@data$AvgQ_cmDay, (LOOCV_Pred0), xlab = "ULTRASeep Meas. Vertical Seep. (cm/day)",
     ylab = "LOOCV prediction (cm/day", pch = 20, cex = 1.5, xlim = c(0, 5), ylim = c(0,5))
lines(c(-100, 100), c(-100, 100), lty = 2, lwd = 1)

#####---------------------------------------------------------------------------
# Remap OK onto hydro grid
nc_grd$VqOK <- NA
nc_grd@data$VqOK_MGY <- NA

kr_sgdf$II <- (kr_sgdf$s1 - 0.5) + 13
kr_sgdf$JJ <- (kr_sgdf$s2 - 0.5) + 33

# remap onto mainstem/turning basin hydro grid
reproj_grd$VqOK <- sapply(1:nrow(reproj_grd), function(x)
  kr_sgdf$VSeepKR.pred[which(kr_sgdf$II == reproj_grd@data$II[x] &
                            kr_sgdf$JJ == reproj_grd@data$JJ[x])])

# remap onto entire NTC hydrogrid
m <- match(reproj_grd$Id, nc_grd$Id)
nc_grd$VqOK[m] <- unlist(reproj_grd$VqOK)
nc_grd$VqOK <- unlist(nc_grd$VqOK)

# Calculate vertical seepage in MGY
p <- lapply(nc_grd@polygons , slot , "Polygons")
for(i in 1:length(p)){
  nc_grd$VqOK_MGY[i] <- unlist(nc_grd$VqOK)[i]*365/100*nc_grd@data$AREA[i]*264.172/1e6 
}
sum(nc_grd$VqOK_MGY, na.rm = T)
#####---------------------------------------------------------------------------
# Save new NTC grid as shapefile for import into ArcGIS
fp <- "C:/Users/thasegawa/Documents/68 NYC DEP Papers/05 Data/Newtown Creek/GC-Density Averaging/Straightened Grid/NTConly_hydrogrid_OKNug"
writeOGR(nc_grd, paste(file.path(fp, "NTConly_hydrogrid_OKNug"), sep= ""),
         "NTConly_hydrogrid_OKNug", driver="ESRI Shapefile")

#####---------------------------------------------------------------------------
# Calculate difference between IDW and ordinary kriging
kr_sgdf$IDW_KRdiff <- sg_sgdf$var1.pred - kr_sgdf$VSeepKR.pred
spplot(kr_sgdf["IDW_KRdiff"])

#####---------------------------------------------------------------------------
#####---------------------------------------------------------------------------
#####---------------------------------------------------------------------------
##### Scratch code.  Not used.
plot(nc_grd)
lines(reproj_grd, col = "blue")
points(us, pch = 20, col = "red")

test <- reproj_grd[which(reproj_grd$II == 13), ]
test <- test[which(test$JJ == 33), ]


# g <- gstat(id="VSeepIDW", formula = AvgQ_cmDay~1, data=data,
#            nmax=7, set=list(idp = .5))
# interpVSEEP <- interpolate(sgRaster, g)
# extract(interpVSEEP, us_str_points_spdfSUB)
# 
# cutoff = 100
# width = cutoff/20
# 
# lm.form = "AvgQ_cmDay ~ 1"
# vgm = variogram(as.formula(lm.form),
#                 data = data, cutoff = cutoff, width=width, alpha = c(0), 
#                 tol.hor = 90) 
# 
# # # Calculate model variogram
# null.vgm <- vgm(var(data$AvgQ_cmDay), "Sph", sqrt(areaSpatialGrid(sg))/4,
#                 nugget=0.002) # initial parameters
# vgm.fit <- fit.variogram(vgm, model=null.vgm)
# plot(vgm, vgm.fit)


sgRaster <- raster(sg_sgdf, layer=1, values=TRUE)

test <- SpatialPoints(matrix(c(nc_grd_over@data$XgridFrac[56], 
                               nc_grd_over@data$YgridFrac[56]), ncol = 2), CRS("+init=EPSG:26918"))
test <- SpatialPoints(matrix(c(103, 0), ncol = 2), CRS("+init=EPSG:26918"))
points(test, col = "blue")
NS_count <- nc_grd[which(nc_grd$JJ == 36), ]
NS_count2 <- NS_count[which(!NS_count$II %in% 119:130), ]
NS_count3 <- nc_grd[which(nc_grd$JJ == 39), ]

plot(nc_grd)
lines(reproj_grd, col = "blue")
points(us, pch = 20, col = "red")
lines(NS_count3, col = "red")

plot(nc_grd_over[56,])
points(us[56,])
points(SpatialPoints(matrix(nc_grd_over_corners[[56]][c(4,1), ], ncol = 2),
                     CRS("+init=EPSG:26918")), col = "red")
par(new = T)
sl <- SpatialLines(list(Lines(Line(matrix(nc_grd_over_corners[[53]][c(4,1), ], ncol = 2)), ID="a")))
lines(sl, col = "green")