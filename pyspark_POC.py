from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression 


class SparkMLPipeline:
    def __init__(self, spark_session):
        self.spark = spark_session

    def read_data(self, file_location):
        """
        Read data from the specified file location.

        Parameters:
        - file_location: Path to the data source (can be a database, S3 bucket, Snowflake, etc.)
        """
        df_pyspark = self.spark.read.csv(file_location, header=True, inferSchema=True)
        return df_pyspark

    def index_categorical_columns(self, df, indx_input_cols, indx_output_cols):
        """
        Index categorical columns.

        Parameters:
        - df: PySpark DataFrame
        - input_cols: List of columns to be indexed
        - output_cols: List of corresponding output columns for indexing
        """
        indexer = StringIndexer(inputCols=indx_input_cols, outputCols=indx_output_cols)
        df_indexed = indexer.fit(df).transform(df)
        return df_indexed

    def assemble_features(self, df, input_cols, output_col):
        """
        Assemble features.

        Parameters:
        - df: PySpark DataFrame
        - input_cols: List of columns to be assembled
        - output_col: Output column for assembled features
        """
        feature_assembler = VectorAssembler(inputCols=input_cols, outputCol=output_col)
        df_assembled = feature_assembler.transform(df)
        return df_assembled

    def train_linear_regression_model(self, train_data):
        """
        Train a linear regression model.

        Parameters:
        - train_data: Training data (PySpark DataFrame)
        """
        regressor = LinearRegression(featuresCol='Independent Features', labelCol='total_bill')
        model = regressor.fit(train_data)
        return model

    def evaluate_model(self, model, test_data):
        """
        Evaluate the performance of the trained model.

        Parameters:
        - model: Trained linear regression model
        - test_data: Test data (PySpark DataFrame)
        """
        prediction = model.evaluate(test_data)
        r_squared = model.summary.r2
        mean_absolute_error = model.summary.meanAbsoluteError
        mean_squared_error = model.summary.meanSquaredError
        pred_results = prediction.predictions
        return pred_results, r_squared, mean_absolute_error, mean_squared_error

    # def store_data_snowflake(self, df, snowflake_options):
    #     """
    #     Store processed data in Snowflake.

    #     Parameters:
    #     - df: PySpark DataFrame
    #     - snowflake_options: Dictionary containing Snowflake connection options
    #     """
    #     try:
    #         # Ensure the necessary options are present
    #         required_options = ["sfURL", "sfUser", "sfPassword", "sfDatabase", "sfWarehouse", "sfSchema", "sfRole"]
    #         for option in required_options:
    #             if option not in snowflake_options:
    #                 raise ValueError(f"Missing required Snowflake option: {option}")

    #         # Write to Snowflake
    #         df.write.format("snowflake").options(**snowflake_options).mode("overwrite").save()
    #         logging.info("Data successfully stored in Snowflake.")

    #     except Exception as e:
    #         logging.error(f"Error storing data in Snowflake: {str(e)}")
# Usage example:
def run_spark_ml_pipeline(file_location, indx_input_cols, indx_output_cols):
    # Create Spark session
    spark_session = SparkSession.builder.appName("SparkMLPipeline").config("spark.kubernetes.master", "k8s://https://spark-dns-x9yrg2tb.hcp.centralus.azmk8s.io").getOrCreate()

    # Create an instance of SparkMLPipeline
    ml_pipeline = SparkMLPipeline(spark_session)

    # Read data and index categorical columns
    df_raw = ml_pipeline.read_data(file_location)
    df_indexed = ml_pipeline.index_categorical_columns(df_raw, indx_input_cols=indx_input_cols, indx_output_cols=indx_output_cols)

    # Assemble features
    feature_cols = ['tip', 'size'] + indx_output_cols
    df_assembled = ml_pipeline.assemble_features(df_indexed, feature_cols, 'Independent Features')

    # # Store processed data in Snowflake
    # ml_pipeline.store_data_snowflake(df_assembled, snowflake_options)
    
    finalized_data = df_assembled.select("Independent Features", "total_bill")
    # Train linear regression model
    train_data, test_data = finalized_data.randomSplit([0.75, 0.25])
    trained_model = ml_pipeline.train_linear_regression_model(train_data)

    # Evaluate model
    pred_results, r_squared, mae, mse = ml_pipeline.evaluate_model(trained_model, test_data)

    # Visualize coefficients, intercept, and performance metrics
    print("Coefficients:", trained_model.coefficients)
    print("Intercept:", trained_model.intercept)
    print("R-Squared:", r_squared)
    print("Mean Absolute Error:", mae)
    print("Mean Squared Error:", mse)
    pred_results.show()

# Example usage:
if __name__ == "__main__":
    file_location = "tips.csv"
    indx_input_cols = ["sex","smoker","day","time"]
    indx_output_cols = ["sex_indexed","smoker_indexed","day_indexed","time_indexed"]

    # snowflake_options = {
    #     "sfURL": "BO48159.snowflakecomputing.com",
    #     "sfUser": "rnadh",
    #     "sfPassword": "Kirkland!12",
    #     "sfDatabase": "SNOWFLAKE_SAMPLE_DATA",
    #     "sfWarehouse": "SPARK_POC",
    #     "sfSchema": "PUBLIC",
    #     "sfRole": "RNADH",
    # }

    run_spark_ml_pipeline(file_location, indx_input_cols, indx_output_cols)