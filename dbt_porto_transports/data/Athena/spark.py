spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions 
--conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog 
--conf spark.sql.catalog.glue_catalog.warehouse=file:///tmp/spark-warehouse
--conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog
--conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO 


--conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog 
--conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog 
--conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO 
--conf spark.sql.catalog.glue_catalog.warehouse=file:///tmp/spark-warehouse
# Run locally
# docker run -it -v ~/.aws:/home/glue_user/.aws -e AWS_PROFILE=personal -e AWS_REGION=eu-central-1 -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 --name glue_pyspark amazon/aws-glue-libs:glue_libs_4.0.0_image_01 pyspark


# Run local notebook 
# JUPYTER_WORKSPACE_LOCATION=~/jupyter_workspace/ 
# docker run -it -v ~/.aws:/home/glue_user/.aws -v $JUPYTER_WORKSPACE_LOCATION:/home/glue_user/workspace/jupyter_workspace/ -e AWS_PROFILE=personal -e AWS_REGION=eu-central-1 -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 -p 8998:8998 -p 8888:8888 --name glue_jupyter_lab amazon/aws-glue-libs:glue_libs_4.0.0_image_01 /home/glue_user/jupyter/jupyter_start.sh
import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1700306411531 = glueContext.create_dynamic_frame.from_catalog(
    database="porto",
    table_name="porto_rawfile_data",
    transformation_ctx="AWSGlueDataCatalog_node1700306411531",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1700309182136_df = AWSGlueDataCatalog_node1700306411531.toDF()
AWSGlueDataCatalog_node1700309182136 = glueContext.write_data_frame.from_catalog(
    frame=AWSGlueDataCatalog_node1700309182136_df,
    database="porto",
    table_name="trip_stops_iceberg",
    additional_options={},
)

job.commit()
