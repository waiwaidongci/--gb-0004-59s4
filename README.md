# 潮汐需求预测席 / demand-tide

面向潮汐鲜花供应协作组的日需求回测、预测与发布工作席。所有客户及业务数据均为合成数据。

24 位计划员原来复制上周需求并手工调整，无法说明误差、区分模型、追溯发布依据。上游日需求明细进入连续日期序列，经滚动回测产生模型比较与未来参考，下游计划员下载 CSV 讨论采购与日配。

## 启动

```sh
cp .env.example .env
docker compose up -d --build
docker compose exec -T backend python -m scripts.seed_demo
```

前端 http://localhost:18203 ，后端 OpenAPI http://localhost:19203/docs ，MySQL localhost:17703。Compose 顶层 name 与显式 container_name 允许在中文、空格路径下启动。退出并移除本项目演示数据：`docker compose down -v --remove-orphans`。

| 账号 | 密码 | 页面与权限 | 典型动作 |
|---|---|---|---|
| admin@tide.demo | Tide2026! | 全部页面、观测及预测写入、发布 | 复核后发布日配建议 |
| analyst@tide.demo | Tide2026! | 全部页面、观测及预测写入；不可发布 | 建立滚动回测任务 |
| viewer@tide.demo | Tide2026! | 预测/台账/档案只读、结果导出；不可看审计 | 阅读计划参考 |

## 一天的工作剧本

1. 08:00 分析师登录，检查 `tide-demand-2026.csv` 的杭州·日配玫瑰 180 天观测。
2. 08:05 在序列台账检查近 42 天变化；缺失日期会阻止预测。
3. 08:10 创建“下周日配 · 杭州玫瑰”，预测 14 天、季节周期 7 天。
4. Redis 入队，由独立 Python worker 执行逐日回测，页面自动刷新状态。
5. 比较季节朴素法与 α=0.2/0.5/0.8 指数平滑的 MAE、WAPE。
6. 查看点预测与残差 10%/90% 分位经验带；突发节假日需求需人工复核。
7. 计划负责人用 admin 记录发布说明并确认，发布档案保留运行关联。
8. 配送联络员用 viewer 阅读并下载带口径说明的预测 CSV。

## 计算口径

`backend/src/services/forecast_algorithm.py` 是独立可复算 Python 算法。输入为连续日需求非负有限序列、horizon 1–30、season 2–30。至少 42 天且不少于 3 个季节。固定种子 42..47 的 seed 生成 6 条、每条 180 天的观测，合计 1080 条。

滚动验证留出最近 min(28,n//3) 天。第 i 天只使用 values[:i]，季节朴素预测为 y[i-season]；指数平滑 l[t]=αy[t]+(1−α)l[t−1]。按回测 MAE 最小者选择候选。WAPE=sum(abs(error))/sum(actual)，分母为 0 返回 null。未来多步用递推值，区间为点预测加验证残差的经验 10%/90% 分位并限制非负。分位带可能整体偏离有偏的点预测，不强制包含点估计。区间覆盖率没有保证，未建模节假日和长期趋势。结果记录输入和 checksum、训练天数、验证天数。短序列、负值、非有限值、日期缺口均失败，前端保留错误并引导重建任务。

## 技术与结构

| 层 | 技术 |
|---|---|
| 页面 | Vue 3.5 / TypeScript / Vite 6 / Vue Router |
| 接口 | Python 3.11 / FastAPI / SQLAlchemy 2 / PyJWT |
| 持久化 | MySQL 8.0；外键与自然唯一键 |
| 队列 | Redis 7；独立 worker 心跳 |
| 入口 | Nginx 1.27；/api/ 剥离后代理后端 |

`frontend/src/{api,stores,types,components/common,hooks,pages,router,utils,constants}`；`backend/src/{routes,controllers,services,models,schemas,middlewares,utils,constants,config}`；种子在 `backend/scripts/seed_demo.py`，结构版本说明在 `backend/migrations/`。测试、截图与真实执行报告位于批次根目录 `test-artifacts/gb-0004/`，源码中不存放测试产物。

共享枚举：Role 和 RunStatus 同时定义在 `backend/src/constants/enums.py`、`frontend/src/constants/enums.ts`；数据库 user.role/run.status 与权限依赖 `middlewares/auth.py`、任务流 `services/run_service.py`/`worker.py` 使用对应字符串。前端 auth store、StatusBadge 和任务页使用枚举口径。SeriesTable 被首页和台账共用，RunTable 被首页和回测共用；PageHeading、ErrorNotice、ForecastChart 多页共用。

## 环境与开发

`.env.example` 列出端口、MySQL 用户/密码、JWT_SECRET 和 SEED_DEMO。`.env` 被忽略。所列密码是可公开的本地合成演示密码，外部部署应通过环境变量替换。`SEED_DEMO=true` 启动插入不存在的自然键，不覆盖修改；失败记日志不阻塞接口。种子可以重复执行。

后端本地：Python 3.11，安装 requirements.txt，配置 DATABASE_URL/REDIS_URL 后 `uvicorn src.main:app --reload`。前端本地：`npm install && npm run dev`，Vite /api 代理到 19203。所有计算、校验及持久化均在后端。请求有 Redis 每分钟限流、全局错误处理、JWT 8 小时失效与写操作审计。

五个 Compose 服务各有 healthcheck：frontend、backend、worker、db、redis。DB/Redis/产物为命名卷；worker 仅本地心跳健康不代表任务成功，任务成功需查看持久化状态。演示 worker 用 Redis BLPOP，处理中进程崩溃的任务暂无自动重投，须重新创建并在结果页确认。

## License

MIT，见 LICENSE。
