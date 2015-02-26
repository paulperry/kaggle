#split training data into several days

from datetime import datetime

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#main program starts here
start = datetime.now()

train = 'train.csv' # path to training file
target_date = '30'
save_file = 'date' + target_date + '.csv'
str_label = 'id,click,hour,C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21'

with open(save_file, 'w') as outfile:
    outfile.write('%s\n' % str_label)

    f=open(train)
    f.readline()
    for line in f:
        xx=line.split(',')
        date = xx[2][4:6]
        if date == target_date :
            outfile.write('%s' % line)

    f.close()

print('saved: %s, etime: %s' % (save_file, str(datetime.now() - start)))
