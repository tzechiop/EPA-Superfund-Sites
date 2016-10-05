##### Function to perform cell declustering of sediment data
### Filename: Point_CellDeclustering.R
### Notes:
############################################################################

# INPUTS:
# cellSize: vector of values indicating the length of a side of the cell (cells are only square)
# spdf: spatialpointsdataframe holding points for declustering

# OUTPUTS:
# CD_df <- data frame of cell declustered averages for various cell sizes

# FUNCTION:

Point_CellDeclustering_v2 <- function(cellSize, spdf, chemical_name){
######------------------------------------------------------------------------------------------------
  #####Cell decluster over entire area
  CD_lst <- list()
  CD_CellWts <- list()
  cellCnt <- vector()
  bb <- bbox(spdf)
  max_side <- round(max(c(diff(bb[1,])+10, diff(bb[2,])+10))) # determine which dimension is largest
  bb1 <- matrix(c(bb[,1], bb[,1]+max_side), ncol = 2) # create new bbox using largest dimension and LL corner of bb
  dm <- data.matrix(spdf@data[, which(names(spdf@data) == chemical_name)])
  for(i in 1:length(cellSize)){
    cs <- rep(max_side/cellSize[i],2) # cell size
    cc <- bb1[, 1] + (cs/2)  # cell offset
    cd <- ceiling(diff(t(bb1))/cs)  # number of cells per direction
    grd <- GridTopology(cellcentre.offset=cc, cellsize=cs, cells.dim=cd)
    sp_grd <- SpatialGridDataFrame(grd,
                                   data=data.frame(id=1:prod(cd)),
                                   proj4string=CRS(proj4string(spdf)))
    
    spdf@data$cellID <- over(spdf, sp_grd)$id
    d <- length(unique(spdf$cellID))
    tableCnt <- table(spdf$cellID)
    
    for(j in 1:length(spdf$cellID)){
      index <- match(spdf@data$cellID[j], as.numeric(names(tableCnt)))
      #spdf$cellCnt[j] <- tableCnt[index] 
      cellCnt[j] <- tableCnt[index]
    }
    #CD_lst[[i]] <- sapply(1:ncol(dm), function(x)  1/d*sum(dm[,x]/spdf@data$cellCnt, na.rm = T))
    CD_lst[[i]] <- sapply(1:ncol(dm), function(x)  1/d*sum(dm[,x]/cellCnt, na.rm = T))
    CD_CellWts[[i]] <- cellCnt
  }
  CD_df <- list("CD_mean" = do.call(rbind, CD_lst), "MinMean_Wts" = CD_CellWts[[order(do.call(rbind, CD_lst))[1]]])

######------------------------------------------------------------------------------------------------
  return(CD_df)
}