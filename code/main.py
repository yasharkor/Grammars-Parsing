# Libraries to be imported
from nltk.parse import ChartParser
from nltk.grammar import CFG
import nltk
import csv
import re
import pandas as pd
import argparse
from sklearn.metrics import classification_report

parser = argparse.ArgumentParser(description='input file name')
parser.add_argument('--input',required=True, help="Please add the input file name path and name")
args = parser.parse_args()


# Read Data from input file given by args.
df=pd.read_csv(args.input, sep='\t',index_col='id')

# Create a output dataframe with the same index as input dataframe and two other columns including ground_truth and prediction - ground_truth is copied from input file
df_out=pd.DataFrame(columns=['ground_truth','prediction'],index=df.index)
df_out['ground_truth']=df['label']

#--------------------------------------------------------------------------#
#---------------------------------------------------------------------------#

nltk.grammar._STANDARD_NONTERM_RE = re.compile(r'( [:\w$`\'.,/-][\w$`\'/^<>-]* ) \s*', re.VERBOSE)
# import grammar from toy.cfg
#---------------------------------------Import grammar from 
grammar=nltk.data.load('../grammars/toy.cfg')
parser = nltk.ChartParser(grammar)
# loop over input dataframe
for index, row in df.iterrows():  
# tokenize the rows of dataframe (pos column)
  tokens = row['pos'].split()
# try to parse the tokens using the given grammar
  try:
    p=list(parser.parse(tokens))
# if len=0 means contains grammar errors and it could not parse - change the output dataframe to 1 
    if len(p) == 0:
        df_out.loc[index,'prediction']=1
    
    else:
# # if len!=0 means correct grammar and it could parse - change the output dataframe to 0
        df_out.loc[index,'prediction']=0

  except ValueError as e:
    df_out.loc[index,'prediction']=1
    print(e)

#-----------------------------------------------------------------------------#
#--------------------------------Save the file--------------------------------#
#-----------------------------------------------------------------------------#

  # Save the output report into tsv file in output directory with name output.tsv file name
df_out.to_csv('../output/output.tsv', sep='\t')


#------------------------------------------------------------------------------#
#-----------------------------Creating classification report-------------------#
#------------------------------------------------------------------------------#

# Print the classification report
print(classification_report(list(df_out['ground_truth']),list(df_out['prediction']),target_names=['Correct grammar','Wrong grammar']))

