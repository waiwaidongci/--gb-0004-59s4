export const Role={ADMIN:'admin',ANALYST:'analyst',VIEWER:'viewer'} as const;
export const RunStatus={QUEUED:'queued',RUNNING:'running',COMPLETED:'completed',FAILED:'failed'} as const;
export const statusLabels:Record<string,string>={queued:'等待计算',running:'正在回测',completed:'已完成',failed:'需处理'};
export const roleLabels:Record<string,string>={admin:'计划负责人',analyst:'预测分析师',viewer:'配送联络员'};
