# Load packages  ------------------------------------------------------------------------------
library(tidyjson)
library(magrittr)
library(stringr)
library(RSQLite)
library(tidyverse)

# Read in and structure data ------------------------------------------------------------------
con = dbConnect(SQLite(),dbname = "../javascript/experiment_1/participants.db");
df.data = dbReadTable(con,"counterfactual_similarity")
dbDisconnect(con)
print(df.data)
#filter out incompletes 
df.data = df.data %>% 
  stats::filter(status %in% 3:5) %>% 
  stats::filter(!str_detect(uniqueid,'debug'))

# demographic data 
df.demographics = df.data$datastring %>% 
  spread_values(condition = jnumber('condition'),
                age = jnumber('questiondata','age'),
                gender = jstring('questiondata','sex'),
                feedback = jstring('questiondata','feedback')
  ) %>% 
  rename(participant = document.id) %>% 
  mutate(time = difftime(df.data$endhit,df.data$beginhit,units = 'mins'))

variables = c('trial','prediction','counterbalance','responsibility_1','responsibility_2')

# trial data 
df.long = df.data$datastring %>% 
  as.tbl_json() %>% 
  spread_values(participant = jstring('workerId')) %>%
  enter_object('data') %>%
  gather_array('order') %>% 
  enter_object('trialdata') %>% 
  gather_array('index') %>% 
  append_values_string('values') %>% 
  as.data.frame() %>% 
  stats::filter(!values %in% c('id','type','predict','prior','counterbalance','NA','right','left','judgement')) %>% 
  spread(index,values) %>%
  select(-c(document.id,order)) %>% 
  setNames(c('participant','trial','rating')) %>% 
  mutate(index = rep(c('criticality','responsibility'),nrow(.)/2)) %>% 
  # spread(index,rating) %>% 
  mutate(trial = trial %>% as.character() %>% as.numeric(),
         participant = factor(participant) %>% as.numeric(),
         rating = as.numeric(rating)) %>% 
  select(participant,trial,index,rating) %>% 
  arrange(participant,trial)

# Plot results  -------------------------------------------------------------------------------

judgment_type = 'responsibility'
# judgment_type = 'criticality'

df.long %>% 
  stats::filter(index == judgment_type) %>% 
  ggplot(aes(x=trial,y=rating))+
  stat_summary(fun.data = mean_cl_boot, geom = 'linerange', size = 0.5)+
  stat_summary(fun.y = mean, geom = 'line', size = 1)+
  stat_summary(fun.y = mean, geom = 'point', size = 2)+
  geom_point(alpha = 0.2, position = position_jitter(width = 0.1, height = 0))+
  # geom_line(aes(group=participant),size=0.5,alpha=0.2)+
  labs(y = judgment_type, x = 'trial')+
  scale_x_continuous(breaks = 0:15,labels = 0:15)+
  theme_bw()+
  theme(text = element_text(size = 20),
        panel.grid = element_blank())
ggsave(paste0("../../figures/plots/",judgment_type,"_judgments.pdf"),width=12,height=4)









