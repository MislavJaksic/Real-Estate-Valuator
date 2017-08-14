## Dataset Transformation

Datasets need to be transformed before being given to a machine algorithm. Positive skewness needs to be
repaired with a natural logarithm, missing values need to be replaced by numpy.nan, values need to be grouped up
and many other transformations need to be performed.

### DatasetTransformer

Responsibilities: accept a pandas DataFrame dataset and perform data transformations on the dataset.

### TransformationScripts

Each dataset has its own script that transforms the dataset into a form that can be given to a machine algorithm.
Scripts use methods provided by the transformer to perform the transformations, but also break encapsulation by
directly accessing the dataset. The dataset is access directly because of a pandas syntax quirk. Note to self:
try to solve it.