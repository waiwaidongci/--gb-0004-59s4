# 初始结构
SQLAlchemy Base.metadata.create_all 建立外键与唯一约束；模型为 schema 的单一来源。
后续结构变更应在此目录新增版本迁移，不依靠 create_all 修改现有列。
唯一键：series.code、observations(series_id,day)、forecast_points(run_id,day)、releases.run_id、users.email。
