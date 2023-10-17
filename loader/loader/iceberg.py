# ruff: noqa: E501
from pyiceberg.catalog import Catalog, load_catalog
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.table.sorting import SortField, SortOrder
from pyiceberg.transforms import (DayTransform, IdentityTransform,
                                  MonthTransform, YearTransform)
from pyiceberg.types import (FloatType, IntegerType, NestedField, StringType,
                             TimestampType)


def create_namespace(catalog: Catalog):

    ns = catalog.list_namespaces()
    print(ns)
    if "porto" not in [n[0] for n in ns]:
        catalog.create_namespace("porto", properties={"location": "s3://porto-realtime/data"})


def create_porto_table(catalog: Catalog):

    schema = Schema(
    NestedField(field_id=1, name="id", field_type=IntegerType(), required=False),
    NestedField(field_id=2, name="stopId", field_type=StringType(), required=True),
    NestedField(field_id=3, name="gtfsId", field_type=StringType(), required=True),
    NestedField(field_id=4, name="lat", field_type=FloatType(), required=False),
    NestedField(field_id=5, name="lon", field_type=FloatType(), required=False),
    NestedField(field_id=6, name="name", field_type=StringType(), required=True),
    NestedField(field_id=7, name="desc", field_type=StringType(), required=True),
    NestedField(field_id=8, name="zoneId", field_type=StringType(), required=True),
    NestedField(field_id=9, name="serviceDay", field_type=IntegerType(), required=False),
    NestedField(field_id=10, name="realtimeState", field_type=StringType(), required=True),
    NestedField(field_id=11, name="realtimeDeparture", field_type=IntegerType(), required=False),
    NestedField(field_id=12, name="scheduledDeparture", field_type=IntegerType(), required=False),
    NestedField(field_id=13, name="realtimeArrival", field_type=IntegerType(), required=False),
    NestedField(field_id=14, name="scheduledArrival", field_type=IntegerType(), required=False),
    NestedField(field_id=15, name="arrivalDelay", field_type=IntegerType(), required=False),
    NestedField(field_id=16, name="departureDelay", field_type=IntegerType(), required=False),
    NestedField(field_id=17, name="realtime", field_type=IntegerType(), required=False),
    NestedField(field_id=18, name="pickupType", field_type=StringType(), required=True),
    NestedField(field_id=19, name="headsign", field_type=StringType(), required=True),
    NestedField(field_id=20, name="trip_id", field_type=StringType(), required=True),
    NestedField(field_id=21, name="trip_gtfsId", field_type=StringType(), required=True),
    NestedField(field_id=22, name="trip_directionId", field_type=StringType(), required=True),
    NestedField(field_id=23, name="trip_tripHeadsign", field_type=StringType(), required=True),
    NestedField(field_id=24, name="route_id", field_type=StringType(), required=True),
    NestedField(field_id=25, name="route_gtfsId", field_type=StringType(), required=True),
    NestedField(field_id=26, name="route_shortName", field_type=StringType(), required=True),
    NestedField(field_id=27, name="route_longName", field_type=StringType(), required=True),
    NestedField(field_id=28, name="route_mode", field_type=StringType(), required=True),
    NestedField(field_id=29, name="route_color", field_type=StringType(), required=True),
    NestedField(field_id=30, name="agency_name", field_type=StringType(), required=True),
    NestedField(field_id=31, name="agency_id", field_type=StringType(), required=True),
    NestedField(field_id=32, name="created_at", field_type=TimestampType(), required=True),
    )

    porto_partition_spec = PartitionSpec(
        PartitionField(field_id=32,source_id=32, transform=YearTransform(), name="created_at_year"),
        PartitionField(field_id=32,source_id=32, transform=MonthTransform(), name="created_at_month"),
        PartitionField(field_id=32,source_id=32, transform=DayTransform(), name="created_at_day")
    )

    sort_order = SortOrder(SortField(source_id=32, transform=IdentityTransform()))


    if "realtime" not in [t[1] for t in catalog.list_tables("porto")]:
        table = catalog.create_table(
            identifier="porto.realtime",
            schema=schema,
            partition_spec=porto_partition_spec,
            sort_order=sort_order,
        )
        return table
    else:
        table = catalog.load_table("porto.realtime")
        return table



if __name__ == "__main__":
    catalog = load_catalog("default", 
    **{
        "s3.region": "eu-west-1"
    })

    table = create_porto_table(catalog)
    print(table.schema())
    print(table.specs())

    scan = table.scan(limit=100)

    pd = scan.to_pandas()
