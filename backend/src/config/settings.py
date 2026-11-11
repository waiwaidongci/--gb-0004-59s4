import os
DATABASE_URL=os.getenv('DATABASE_URL','mysql+pymysql://tide:tide_demo_2026@localhost:17703/demand_tide')
REDIS_URL=os.getenv('REDIS_URL','redis://localhost:6379/0')
JWT_SECRET=os.getenv('JWT_SECRET','tide-local-demo-change-before-sharing')
