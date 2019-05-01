import numpy as np
import pandas as pd
import numpy.matlib
# from skimage import io
from itertools import combinations
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from mpl_toolkits.mplot3d import Axes3D # Not used but needed to make 3D plots


all_features = ['rural_urban', 'urban_influence', 'high_school_degree_percent',
            'politics', 'percent_pov_child', 'percent_pov_all', 'employment_rate',
            'med_household_income_2017', 'white_county', 'white_school', 'grade_span',
            'male_percent', 'num_free_reduced_meals', 'total_percent_absences',
            'low_income_absence_percent', 'religious_exempt',
            'personal_exempt', 'medical_exempt', 'school_district', 'immunization_rate']

real_all_features = ['rural_urban', 'urban_influence', 'high_school_degree_percent',
            'politics', 'percent_pov_child', 'percent_pov_all', 'employment_rate',
            'med_household_income_2017', 'white_county', 'white_school', 'grade_span',
            'male_percent', 'num_free_reduced_meals', 'total_percent_absences',
            'low_income_absence_percent', 'religious_exempt',
            'personal_exempt', 'medical_exempt', 'immunization_rate']
possible_features = ['rural_urban', 'urban_influence', 'high_school_degree_percent',
            'politics', 'percent_pov_child', 'percent_pov_all', 'employment_rate',
            'med_household_income_2017', 'white_county', 'white_school', 'grade_span',
            'male_percent', 'num_free_reduced_meals', 'total_percent_absences',
            'low_income_absence_percent', 'religious_exempt',
            'personal_exempt', 'medical_exempt']
all_combos = list(combinations(possible_features, 2))

# all_features = ['religious_exempt', 'white_school', 'immunization_rate', 'school_district']
# real_all_features = all_features[0:-1]
labels=['school_name']
# labels = ['immunization_rate']

def preprocess_features():
    df = pd.read_csv('./complete_with_school_cleaned.csv')
    print(df.columns.values)
    df['med_household_income_2017'] = df['med_household_income_2017'].str.replace('$','')
    string_columns = ['high_school', 'clinton', 'trump', 'med_household_income_2017',
                      'employed_2015', 'labor_total_2015', 'labor_total_2016',
                      'employed_2016']
    for column in string_columns:
        df[column] = pd.to_numeric(df[column].str.replace(',',''))
    percent_columns = ['total_percent_absences', 'low_income_absence_percent']
    for column in percent_columns:
        df[column] = pd.to_numeric(df[column].str.replace('%',''))

    df['high_school_degree_percent'] = (1 - (df['high_school'] / df['totalPop'])).multiply(100).round(1)
    df['politics'] = (df['clinton'] / (df['clinton'] + df['trump'])).round(2)
    # corresponding year
    df['employment_rate'] = (df['employed_2015'] / df['labor_total_2015']).multiply(100).round(1)
    df.loc[df['school_year'] == 2016, 'employment_rate'] = (df['employed_2016'] /
                                                            df['labor_total_2016']).multiply(100).round(1)
    df.loc[df['school_year'] == 2017, 'employment_rate'] = (df['employed_2017'] /
                                                            df['labor_total_2017']).multiply(100).round(1)


    df['white_county'] = df['white']
    df['white_school'] = (df['school_white'] / df['total_enrollment']).multiply(100).round(1)
    df['grade_span'] = df['end_grade'] - df['start_grade']
    df['male_percent'] = (df['male'] / df['total_enrollment']).multiply(100).round(1)

    label_encoder = LabelEncoder()
    df['school_district'] = np.array(label_encoder.fit_transform(df['school_district'].values))
    df['school_name'] = np.array(label_encoder.fit_transform(df['school_name'].values))

    df['immunization_rate'] = (df['all_immunizations'] / df['k12_enrollment']).multiply(100).round(1)
    df = df[all_features + labels]
    return df 


def sk_learn_cluster(X, Y, K):
	skmeans = KMeans(n_clusters=K).fit(X)
	predictions = skmeans.predict(X)
	clusters = skmeans.cluster_centers_
	return (clusters, predictions)



def plot_clusters(document_topics, features, centers, clusters):
	"""
	Uses matplotlib to plot the clusters of documents

	Args:
		document_topics: a dictionary that maps document IDs to topics.
		clusters: the predicted cluster for each document.
		centers: the coordinates of the center for each cluster.
	"""
	topics = document_topics
	# topics = np.array([x for x in document_topics.values()])

	ax = plt.figure().add_subplot(111, projection='3d')

	ax.scatter(topics[:, 0], topics[:, 1], topics[:, 2], c=clusters, alpha=0.7) # Plot the documents
	ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], c='black', alpha=1) # Plot the centers
	ax.set_xlabel(features[0])
	ax.set_ylabel(features[1])
	ax.set_zlabel('Immunization Rate')
	plt.tight_layout()
	str_features = features[0] + "_" + features[1]

	plt.savefig('cluster_result/'+str_features+'_scatterplot')


# def plot_word_clusters(data, labels, centroids, centroid_indices):
# 	"""
# 	DO NOT CHANGE ANYTHING IN THIS FUNCTION

# 	You can use this function to plot the words and centroids to visualize your code. 
# 	Points with the same color are considered to be in the same cluster.

# 	:param data - the data set stores as a 2D np array (given in the main function stencil)
# 	:param centroids - the coordinates that represent the center of the clusters
# 	:param centroid_indices - the index of the centroid that corresponding data point it closest to

# 	NOTE: function only works for K <= 5 clusters
# 	"""
# 	# X = df[all_features].values
# 	Y = labels
# 	x = data[:,0].astype(np.float)
# 	y = data[:,1].astype(np.float)
# 	z = data[:,2].astype(np.float)
# 	fig, ax = plt.subplots()
# 	for c in centroids:
# 		x = np.append(x,c[0])
# 		y = np.append(y,c[1])
# 		z = np.append(z, c[2])
# 	try:
# 		colors = {0: 'red', 1: 'yellow', 2: 'blue', 3: 'green', 4: 'brown'}
# 		color = [colors[l] for l in centroid_indices]
# 		for i in range(len(centroids)):
# 			color.append('black')
# 	except KeyError:
# 		print ("Keep to less than 5 clusters")
# 		return
# 	# for i, txt in enumerate(Y):
# 	# 	ax.annotate(txt, (x[i], y[i]))
# 	plt.scatter(x,y,z, c = color)
# 	# plt.xlabel('Neutral --> Polarizing')
# 	# plt.ylabel('Negative --> Positive')
# 	plt.show()

def main():
	df = preprocess_features()
	# all_features = []
	# real_all_features = []
	for x in all_combos:
		all_features = list(x) + ['immunization_rate', 'school_district']
		real_all_features = all_features[0:-1]
		print(real_all_features)

		new_df = df.groupby(['school_district']).mean()
		print(new_df)
		# print(list(df.columns.values))
		# print(df)

		X = new_df[real_all_features].values
		y = new_df[labels].values
		# print(X)
		# pca = PCA(n_components=2).fit(X)
		# X = pca.transform(X)

		clusters, predictions = sk_learn_cluster(X, y, 3)
		plot_clusters(X, x, clusters, predictions)

	# print(df)



if __name__ == "__main__":
    main()