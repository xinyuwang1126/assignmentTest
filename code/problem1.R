setwd("/Users/xinyuwang/Desktop/CSE6740ML/homework3_data")
data=read.csv("MLR.csv",header=FALSE)
X=data[1:1000,1:30]
X=data.matrix(X)
Y=cbind(data[1:1000,31])
beta=matrix(0,30,1)
n=1000
learn_rate=round(n/norm(t(X)%*%X,type="2"),2)
conv_threshold<-1e-10
max_iter<-5000
i=1
iter<-NULL
f_beta<-NULL

f_old<-norm((Y-X%*%beta),type="2")*norm((Y-X%*%beta),type="2")/(2*n)
beta_new<-beta-learn_rate*(t(X)%*%X%*%beta-t(X)%*%Y)/n
beta<-beta_new
f<-norm((Y-X%*%beta),type="2")*norm((Y-X%*%beta),type="2")/(2*n)
f_beta<-c(f_beta,f)
iter<-c(iter,i)
i<-i+1




while(abs(f-f_old)>conv_threshold&&i<=max_iter)
{
  beta_new<-beta-learn_rate*(t(X)%*%X%*%beta-t(X)%*%Y)/n
  beta<-beta_new
  f_old<-f
  f<-norm((Y-X%*%beta),type="2")*norm((Y-X%*%beta),type="2")/(2*n)
  f_beta<-c(f_beta,f)
  iter<-c(iter,i)
  i<-i+1
}
plot(iter,f_beta)
lines(iter,f_beta)

true_beta=read.csv("True_Beta.csv",header=FALSE)
true_beta=data.matrix(true_beta)
error=beta-true_beta
MSE=norm(error,type="2")*norm(error,type="2")/30

