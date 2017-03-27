setwd("/Users/xinyuwang/Desktop/CSE6740ML/homework3_data")
data=read.csv("MLR.csv",header=FALSE)
X=data[1:1000,1:30]
X=data.matrix(X)
Y=cbind(data[1:1000,31])
beta=matrix(0,30,1)
n=1000
i=1

learn_rate=1/(norm(t(X)%*%X,type="2"))
conv_threshold<-1e-10
max_iter<-5000
iter<-NULL
g_beta<-NULL

g_old<-0
m<-1
while(m<1001)
{
  x<-X[m,1:30]
  y<-Y[m,1]
  g_old<-g_old+norm((y-t(x)%*%beta),type="2")*norm((y-t(x)%*%beta),type="2")/2
  m<-m+1
}
g_old<-g_old/n

j=round(runif(1,1,1000))
x=X[j,1:30]
y=Y[j,1]
beta_new<-beta-learn_rate*t(((t(x)%*%beta-y)%*%x))
beta<-beta_new

g<-0
m<-1
while(m<1001)
{
  x<-X[m,1:30]
  y<-Y[m,1]
  g<-g+norm((y-t(x)%*%beta),type="2")*norm((y-t(x)%*%beta),type="2")/2
  m<-m+1
}
g<-g/n
g_beta<-c(g_beta,g)
iter<-c(iter,i)
i<-i+1




while(abs(g-g_old)>conv_threshold&&i<=max_iter)
{
  j=round(runif(1,1,1000))
  x=X[j,1:30]
  y=Y[j,1]
  beta_new<-beta-learn_rate*t(((t(x)%*%beta-y)%*%x))
  beta<-beta_new
  g_old<-g
  
  g<-0
  m<-1
  while(m<1001)
  {
    x<-X[m,1:30]
    y<-Y[m,1]
    g<-g+norm((y-t(x)%*%beta),type="2")*norm((y-t(x)%*%beta),type="2")/2
    m<-m+1
  }
  g<-g/n
  g_beta<-c(g_beta,g)
  iter<-c(iter,i)
  i<-i+1
}
plot(iter,g_beta)
lines(iter,g_beta)

true_beta=read.csv("True_Beta.csv",header=FALSE)
true_beta=data.matrix(true_beta)
error=beta-true_beta
MSE=norm(error,type="2")*norm(error,type="2")/30

