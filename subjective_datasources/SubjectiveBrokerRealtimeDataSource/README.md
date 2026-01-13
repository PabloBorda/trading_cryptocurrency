# SubjectiveBrokerRealtimeDataSource

Subjective datasource implementation for SubjectiveBrokerRealtimeDataSource.

## Usage

```python
from subjective_datasources.SubjectiveBrokerRealtimeDataSource import SubjectiveBrokerRealtimeDataSource

source = SubjectiveBrokerRealtimeDataSource(params={})
source.fetch()
```

## Parameters

Use the params dictionary when constructing the datasource to provide connection and runtime values.
Refer to get_connection_data() for required fields.
