import time
from subjective_abstract_data_source_package.SubjectiveDataSource import SubjectiveDataSource
from brainboost_data_source_logger_package.BBLogger import BBLogger


class SubjectivePublicMarketDataImportDataSource(SubjectiveDataSource):
    connection_type = "FileImport"
    connection_fields = ["source_directory", "file_pattern", "format"]
    icon_svg = "<svg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><circle cx='12' cy='12' r='9' fill='#2d6a4f'/><path d='M7 12h10' stroke='#ffffff' stroke-width='2'/></svg>"

    def get_icon(self):
        return self.icon_svg

    def get_connection_data(self):
        return {"connection_type": self.connection_type, "fields": list(self.connection_fields)}

    def start(self):
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        from com_goldenthinker_trade_datasource_network.TickerSocketAllSymbols import TickerSocketAllSymbols

        ticker = TickerSocketAllSymbols(exchange=ExchangeConfiguration.get_default_exchange(), local_source=True)
        ticker.start()

    def fetch(self):
        if self.status_callback:
            self.status_callback(self.get_name(), "import_started")
        self.start()
        self.set_fetch_completed(True)
        BBLogger.log(f"Import started for {self.get_name()}")
