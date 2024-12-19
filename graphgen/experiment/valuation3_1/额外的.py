import pandas as pd
pd.set_option('display.max_columns', None)
df = pd.read_excel("../data/去除基础镜像结果表.xlsx", index_col=0)
# print(df.describe())
new_df = df[["project"]]
new_df["tool_extra"]= df["tool_result_size"] - df["tool_correct_amount"]
new_df["text_extra"]= df["text_result_size"] - df["text_correct_amount"]
new_df["wxyy_extra"]= df["wxyy_result_size"] - df["wxyy_correct_amount"]

print(new_df.describe())
