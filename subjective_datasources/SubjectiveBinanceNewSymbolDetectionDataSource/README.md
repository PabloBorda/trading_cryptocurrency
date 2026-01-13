# SubjectiveNewSymbolDetectionDataSource

Subjective datasource implementation for SubjectiveNewSymbolDetectionDataSource.

## Usage

```python
from subjective_datasources.SubjectiveBinanceNewSymbolDetectionDataSource import SubjectiveNewSymbolDetectionDataSource

source = SubjectiveNewSymbolDetectionDataSource(params={})
source.fetch()
```

## Parameters

Use the params dictionary when constructing the datasource to provide connection and runtime values.
Refer to get_connection_data() for required fields.
