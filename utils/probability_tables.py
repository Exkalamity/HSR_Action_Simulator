import pandas as pd
import numpy as np

def make_state_table():
    df = pd.read_csv("utils\probability_data\State_Prob_Given_Drawn_Tiles.csv")
    df = df.set_index("Tiles Drawn")
    df = df.iloc[:, ::-1]
    return df

def make_sp_table():
    df = pd.read_csv("utils\probability_data\Average_SP_Used_Given_State.csv")
    states = df["State"].values
    df_T = df.T
    df_T.columns = states
    df_T = df_T.drop(df_T.index[0])
    return df_T

def make_fail_table():
    df =  pd.read_csv("utils\probability_data\Prob_Failure_Per_SP_Given_State.csv")
    states = df["State"].values
    df_T = df.T
    df_T.columns = states
    df_T = df_T.drop(df_T.index[0])
    return df_T

def make_success_table():
    df = pd.read_csv("utils\probability_data\Prob_Success_Per_SP_Given_State.csv")
    states = df["State"].values
    df_T = df.T
    df_T.columns = states
    df_T = df_T.drop(df_T.index[0])
    return df_T
    
def make_transition_matrix():
    df = pd.read_csv("utils\probability_data\Transition_Matrix.csv", index_col=0)
    return df