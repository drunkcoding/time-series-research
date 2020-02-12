library(dplyr)
library(readr)
library(tidyr)

step_list = c(5, 10, 20, 40, 60, 120, 245)
len_slist = length(step_list)
tb_sse = read_csv("000001.SH.txt", col_types = cols(date = col_date(format = "%Y-%m-%d")))
names(tb_sse)[4] = "sh_index"
tb_sse = select(tb_sse, date, sh_index)

dcca_dist = function(x, y, step){
  total_data = inner_join(x,y,by="date")
  total_data = select(total_data, -date)
  total_data = mutate(total_data, close.x = c(NA, diff(log(close.x))))
  total_data = mutate(total_data, close.y = c(NA, diff(log(close.y))))
  total_data = drop_na(total_data)
  total_data = mutate(total_data, close.x = cumsum(close.x-mean(close.x)))
  total_data = mutate(total_data, close.y = cumsum(close.y-mean(close.y)))

  data_size = length(total_data$close.x)
  total_data = mutate(total_data, fit_base=seq(1,data_size))
  # print(head(total_data))
  var.xy = numeric()
  var.x = numeric()
  var.y = numeric()

  for (i in seq(1,data_size-step)){
    end_slice = i+step-1
    tb_slice = total_data[i:end_slice,]
    # print(head(tb_slice))
    x_diff = tb_slice$close.x - predict(lm(close.x ~ fit_base, data = tb_slice), tb_slice["fit_base"])
    y_diff = tb_slice$close.y - predict(lm(close.y ~ fit_base, data = tb_slice), tb_slice["fit_base"])
    var.xy = c(var.xy, mean(x_diff*y_diff))
    var.x = c(var.x, mean(x_diff*x_diff))
    var.y = c(var.y, mean(y_diff*y_diff))
  }
  #print(mean(var.xy))
  #print(mean(var.x)*mean(var.y))
  print(sqrt(2*(1-mean(var.xy)/sqrt(mean(var.x)*mean(var.y)))))
  sqrt(2*(1-mean(var.xy)/sqrt(mean(var.x)*mean(var.y)))) 
}

dpxa_dist = function(x, y, step){
  total_data = inner_join(x,y,by="date")
  total_data = inner_join(total_data, tb_sse, by="date")
  total_data = select(total_data, -date)
  total_data = mutate(total_data, close.x = c(NA, diff(log(close.x))))
  total_data = mutate(total_data, close.y = c(NA, diff(log(close.y))))
  total_data = mutate(total_data, sh_index = c(NA, diff(log(sh_index))))
  total_data = drop_na(total_data)
  total_data = mutate(total_data, fit_base=seq(1,length(total_data[[1]])))
  data_size = length(total_data$close.x)
  # print(data_size)
  
  var.xy = numeric()
  var.x = numeric()
  var.y = numeric()

  for (i in seq(1,data_size-step)){
    end_slice = i+step-1
    tb_slice = total_data[i:(i+step-1),]
    # zfit_base = z_profile[i,end_slice]
    x_rdiff = cumsum(tb_slice$close.x - predict(lm(close.x ~ sh_index, data = tb_slice), tb_slice["sh_index"]))
    y_rdiff = cumsum(tb_slice$close.y - predict(lm(close.y ~ sh_index, data = tb_slice), tb_slice["sh_index"]))
    x_diff = x_rdiff - predict(lm(x_rdiff ~ tb_slice$fit_base), tb_slice["fit_base"])
    y_diff = y_rdiff - predict(lm(y_rdiff ~ tb_slice$fit_base), tb_slice["fit_base"])
    # result = mean(x_diff*y_diff)/sqrt(mean(x_diff*x_diff)*mean(y_diff*y_diff))
    var.xy = c(var.xy, mean(x_diff*y_diff))
    var.x = c(var.x, mean(x_diff*x_diff))
    var.y = c(var.y, mean(y_diff*y_diff))
  }
  print(sqrt(2*(1-mean(var.xy)/sqrt(mean(var.x)*mean(var.y)))))
  sqrt(2*(1-mean(var.xy)/sqrt(mean(var.x)*mean(var.y))))
}


csv_files = list.files(pattern="*.csv")
print(csv_files)
tbl = lapply(csv_files, function(x) read_csv(x, col_types = cols(date = col_date(format = "%Y-%m-%d"))))

tbl = lapply(tbl, function(x) select(x, date, close, code))

for (i in 1:26){
  names(tbl)[i] = tbl[[i]][[3]][1]
  # names(tbl[[i]])[2] = tbl[[i]][[3]][1]
}
tbl = lapply(tbl, function(x) select(x, -code))

for (step in step_list){
  up_df_dpxa = data.frame(matrix(NA,ncol = length(names(tbl)),nrow = length(names(tbl))), row.names = names(tbl))
  #up_df_dcca = data.frame(matrix(NA,ncol = length(names(tbl)),nrow = length(names(tbl))), row.names = names(tbl))
  dn_df_dpxa = data.frame(matrix(NA,ncol = length(names(tbl)),nrow = length(names(tbl))), row.names = names(tbl))
  #dn_df_dcca = data.frame(matrix(NA,ncol = length(names(tbl)),nrow = length(names(tbl))), row.names = names(tbl))
  
  names(up_df_dpxa) = names(tbl)
  #names(up_df_dcca) = names(tbl)
  names(dn_df_dpxa) = names(tbl)
  #names(dn_df_dcca) = names(tbl)
  for (i in 1:25){
    for (j in (i+1):26){
      # print(dfl_dist_dcca[as.character(step)])
      tb_x.up = tbl[[i]][tbl[[i]]$date <= as.Date('2015-05-15'),]
      tb_x.dn = tbl[[i]][tbl[[i]]$date > as.Date('2015-05-15'),]
      tb_y.up = tbl[[j]][tbl[[j]]$date <= as.Date('2015-05-15'),]
      tb_y.dn = tbl[[j]][tbl[[j]]$date > as.Date('2015-05-15'),]
      
      #up_df_dcca[j,i] = dcca_dist(tb_x.up,tb_y.up,step)
      up_df_dpxa[j,i] = dpxa_dist(tb_x.up,tb_y.up,step)
      #dn_df_dcca[j,i] = dcca_dist(tb_x.dn,tb_y.dn,step)
      dn_df_dpxa[j,i] = dpxa_dist(tb_x.dn,tb_y.dn,step)
    }
  }
  #write.csv(up_df_dcca, file =paste0(as.character(step), ".up_dcca"))
  write.csv(up_df_dpxa, file =paste0(as.character(step), "-up-dpxa"))
  #write.csv(dn_df_dcca, file =paste0(as.character(step), ".dn_dcca"))
  write.csv(dn_df_dpxa, file =paste0(as.character(step), "-dn-dpxa"))
}



#tb_data = Reduce(function(dtf1,dtf2) left_join(dtf1,dtf2,by="date"), tbl)
#tb_data = tb_data[complete.cases(tb_data), ]
#for (tb in tbl){ 
#  names(tb)[2] = tb[[3]][1]
#  print(names(tb))
#}
#names(tbl[[1]])
#gather(tbl[[1]], stock, price, -date)
#tbl = lapply(tbl, function(x) gather(x, stock, price, -date))


