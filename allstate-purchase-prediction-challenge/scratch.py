df_predicted_E_1 = pd.read_csv(csv_dir + 'E_1-predicted.csv')
df_predicted_E_1.rename(columns={'Full Model 100%':1}, inplace=True)

df_E_is = df_test_E_is_1[[1]]
s_E_predicted = (df_E_is[[1]] > 0.50).astype(int)
df_E_predicted = pd.DataFrame(s_E_predicted).set_index(df_test_last.index)
df_E_predicted.columns=['E']

df_predicted_F_0 = pd.read_csv(save_dir + 'F_0-predicted.csv')
df_predicted_F_0.rename(columns={'Full Model 100%':0}, inplace=True)
df_predicted_F_1 = pd.read_csv(save_dir + 'F_1-predicted.csv')
df_predicted_F_1.rename(columns={'Full Model 100%':1}, inplace=True)
df_predicted_F_2 = pd.read_csv(save_dir + 'F_2-predicted.csv')
df_predicted_F_2.rename(columns={'Full Model 100%':2}, inplace=True)
df_predicted_F_3 = pd.read_csv(save_dir + 'F_3-predicted.csv')
df_predicted_F_3.rename(columns={'Full Model 100%':3}, inplace=True)

df_F_is = pd.concat([df_predicted_F_0[[1]],
                     df_predicted_F_1[[1]],
                     df_predicted_F_2[[1]],
                     df_predicted_F_3[[1]]], 
                    axis=1)
s_F_predicted = df_F_is.idxmax(axis=1)
df_F_predicted = pd.DataFrame(s_F_predicted).set_index(df_test_last.index)
df_F_predicted.columns=['F']

df_predicted_G_1 = pd.read_csv(save_dir + 'G_1-predicted.csv')
df_predicted_G_1.rename(columns={'Full Model 100%':1}, inplace=True)
df_predicted_G_2 = pd.read_csv(save_dir + 'G_2-predicted.csv')
df_predicted_G_2.rename(columns={'Full Model 100%':2}, inplace=True)
df_predicted_G_3 = pd.read_csv(save_dir + 'G_3-predicted.csv')
df_predicted_G_3.rename(columns={'Full Model 100%':3}, inplace=True)
df_predicted_G_4 = pd.read_csv(save_dir + 'G_4-predicted.csv')
df_predicted_G_4.rename(columns={'Full Model 100%':4}, inplace=True)

df_G_is = pd.concat([df_predicted_G_1[[1]],
                     df_predicted_G_2[[1]],
                     df_predicted_G_3[[1]],
                     df_predicted_G_4[[1]]], axis=1)
s_G_predicted = df_G_is.idxmax(axis=1)
df_G_predicted = pd.DataFrame(s_G_predicted).set_index(df_test_last.index)
df_G_predicted.columns=['G']
