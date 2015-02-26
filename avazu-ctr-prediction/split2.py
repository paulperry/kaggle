#split training data into several days

from datetime import datetime

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#main program starts here
start = datetime.now()

train = 'train.csv' # path to training file
save_file = 'train_10.csv'
str_label = 'id,click,hour,C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21'

with open(save_file, 'w') as outfile:
    outfile.write('%s\n' % str_label)

    f=open(train)
    f.readline()
    c = 0
    for line in f:
        c += 1
        if c % 10 == 0 :
            outfile.write('%s' % line)

    f.close()

print('saved: %s, etime: %s' % (save_file, str(datetime.now() - start)))
