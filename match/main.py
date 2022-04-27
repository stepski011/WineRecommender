import recordlinkage
from recordlinkage.datasets import load_febrl1
import pandas as pd

def second_method():
    df = pd.read_csv('C:/Users/zoran/Desktop/DI/Wines-FinalDS.csv', sep=',')

    # Indexation step
    indexer = recordlinkage.Index()
    indexer.full()
    #indexer.block(left_on='Wein:')
    candidate_links = indexer.index(df)

    # Comparison step
    compare_cl = recordlinkage.Compare()

    compare_cl.exact('Jahrgang:', 'Jahrgang:', label='Jahrgang:')
    compare_cl.string('Hersteller:', 'Hersteller:', method='jarowinkler', threshold=0.6, label='Hersteller:')
    compare_cl.exact('Wein:', 'Wein:', label='Wein:')
    compare_cl.exact('Erzeugnis aus:', 'Erzeugnis aus:', label='Erzeugnis aus:')
    compare_cl.string('Region:', 'Region:', method='jarowinkler', threshold=0.8, label='Region:')

    features = compare_cl.compute(candidate_links, df)

    # Classification step
    matches = features[features.sum(axis=1) > 3]
    print("Number of matches: " + str(len(matches)))


def first_method():
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    second_method();




