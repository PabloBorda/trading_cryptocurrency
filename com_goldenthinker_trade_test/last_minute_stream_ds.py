from com_goldenthinker_trade_datasource.LastMinuteSymbolStreamDataSource import LastMinuteSymbolStreamDataSource
from com_goldenthinker_trade_datasource.DataSourceManager import DataSourceManager
from com_goldenthinker_trader_robot.Robot import Robot

robot = Robot()

last_min_sequences_all_symbols = DataSourceManager.get_data_source('last_min_sequences_all_symbols')
last_min_sequences_all_symbols.subscribe(robot)
last_min_sequences_all_symbols.start()